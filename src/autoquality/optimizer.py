__all__ = [
    'AutoQuality',
    'DEFAULT_DISTRIBUTIONS'
]

import attr
import datetime
import itertools
import logging
import pandas as pd
import random
import time

from copy import deepcopy
from decimal import Decimal
from scipy import stats
from sklearn.model_selection import ParameterSampler
from typing import Optional, Callable, Dict, List, Any

from ..client import Pool, Task, TolokaClient
from ..client.actions import RestrictionV2, SetSkill
from ..client.assignment import GetAssignmentsTsvParameters
from ..client.collectors import AnswerCount, AssignmentSubmitTime, CollectorConfig, MajorityVote, GoldenSet
from ..client.conditions import (
    AssignmentsAcceptedCount,
    FastSubmittedCount,
    TotalSubmittedCount,
    TotalAnswersCount,
    IncorrectAnswersRate,
    GoldenSetIncorrectAnswersRate
)
from ..client.filter import FilterAnd, FilterOr, Skill
from ..client.quality_control import QualityControl
from .scoring import default_calc_scores, default_calc_ranks

logger = logging.getLogger(__name__)


def _create_autoquality_pool_default(autoquality: 'AutoQuality', params: Dict[str, Any], private_name: str):
    def _replace_or_create_collector_config(
        pool: Pool,
        collector: CollectorConfig,
        rule: QualityControl.QualityControlConfig.RuleConfig
    ) -> Pool:
        for config in pool.quality_control.configs:
            if type(config.collector_config) is type(collector):
                config.rules = [rule]
                return pool

        pool.quality_control.add_action(collector, rule.action, rule.conditions)
        return pool

    def _configure_quality_control_from_params(pool: Pool) -> Pool:

        if 'overlap' in params:
            overlap = params['overlap']
            pool.defaults = Pool.Defaults(
                default_overlap_for_new_task_suites=overlap,
            )
        else:
            overlap = pool.defaults.default_overlap_for_new_task_suites

        if 'AssignmentSubmitTime' in params:
            history_size = int(params['AssignmentSubmitTime']['history_size'])
            avg_page_seconds = int(params['AssignmentSubmitTime']['avg_page_seconds'])
            too_fast_fraction = float(params['AssignmentSubmitTime']['too_fast_fraction'])

            fast_submit_threshold_seconds = int(avg_page_seconds * too_fast_fraction)
            fast_submitted_count = history_size
            fast_submitted_count = min(
                fast_submitted_count,
                history_size,
            )

            pool = _replace_or_create_collector_config(
                pool,
                AssignmentSubmitTime(
                    history_size=history_size,
                    fast_submit_threshold_seconds=fast_submit_threshold_seconds
                ),
                QualityControl.QualityControlConfig.RuleConfig(
                    conditions=[
                        TotalSubmittedCount >= history_size,
                        FastSubmittedCount >= fast_submitted_count
                    ],
                    action=RestrictionV2(
                        scope='POOL',
                        duration=1,
                        duration_unit='DAYS',
                        private_comment='AssignmentSubmitTime',
                    ),
                )
            )

        if 'MajorityVote' in params:
            history_size = params['MajorityVote']['history_size']
            answer_threshold = overlap - 1
            incorrect_answers_rate = params['MajorityVote']['incorrect_answers_rate']

            pool = _replace_or_create_collector_config(
                pool,
                MajorityVote(
                    answer_threshold=answer_threshold,
                    history_size=history_size,
                ),
                QualityControl.QualityControlConfig.RuleConfig(
                    conditions=[
                        TotalAnswersCount >= history_size,
                        IncorrectAnswersRate > incorrect_answers_rate,
                    ],
                    action=RestrictionV2(
                        scope='POOL',
                        duration=1,
                        duration_unit='DAYS',
                        private_comment='MajorityVote',
                    ),
                )
            )

        if 'GoldenSet' in params:
            history_size = params['GoldenSet']['history_size']
            incorrect_answers_rate = params['GoldenSet']['incorrect_answers_rate']

            pool = _replace_or_create_collector_config(
                pool,
                GoldenSet(history_size=history_size),
                QualityControl.QualityControlConfig.RuleConfig(
                    conditions=[GoldenSetIncorrectAnswersRate >= incorrect_answers_rate],
                    action=RestrictionV2(
                        scope='POOL',
                        duration=1,
                        duration_unit='DAYS',
                        private_comment='GoldenSet',
                    )
                )
            )

        if 'TrainingRequirement' in params:
            training_passing_skill_value = params['TrainingRequirement']['training_passing_skill_value']
            pool.quality_control.training_requirement = QualityControl.TrainingRequirement(
                training_pool_id=autoquality.training_pool_id,
                training_passing_skill_value=training_passing_skill_value,
            )

        if 'ExamRequirement' in params and autoquality.exam_skill_id:
            pool = _configure_exam(
                pool,
                autoquality.exam_skill_id,
                params['ExamRequirement']['exam_passing_skill_value']
            )

        return pool

    def _configure_exam(pool: Pool, exam_skill_id, exam_passing_skill_value) -> Pool:
        exam_filter = (Skill(exam_skill_id) >= exam_passing_skill_value)
        if pool.filter is None:
            pool.filter = exam_filter
            return pool

        if not isinstance(pool.filter, FilterAnd):
            pool.filter = FilterAnd([pool.filter])

        has_filter = False
        for filter in pool.filter:
            if isinstance(filter, (FilterOr, FilterAnd)):
                sub_filters = list(filter)
                filter = sub_filters[0] if len(sub_filters) == 1 else filter
            if isinstance(filter, Skill) and filter.key == exam_skill_id:
                filter.value = exam_passing_skill_value
                has_filter = True

        if not has_filter:
            pool.filter &= exam_filter
        return pool

    pool = autoquality.toloka_client.clone_pool(autoquality.base_pool_id)
    pool = _configure_quality_control_from_params(pool)
    pool.private_name = private_name
    pool = autoquality.toloka_client.update_pool(pool.id, pool)
    skill_name = pool.private_name
    autoquality.autoquality_pool_skills[pool.id] = autoquality._create_skill_if_not_exists(skill_name)
    return pool


DEFAULT_DISTRIBUTIONS = dict(
    overlap=stats.planck(0.8, loc=2),
    AssignmentSubmitTime=dict(
        history_size=[5],
        avg_page_seconds=[90],
        too_fast_fraction=stats.skewnorm(a=2, loc=0.2, scale=0.15),
    ),
    MajorityVote=dict(
        history_size=[5],
        incorrect_answers_rate=stats.norm(loc=60, scale=15),
    ),
    GoldenSet=dict(
        history_size=[5],
        incorrect_answers_rate=stats.norm(loc=60, scale=15),
    ),
    TrainingRequirement=dict(
        training_passing_skill_value=stats.norm(loc=50, scale=20),
    ),
    ExamRequirement=dict(
        exam_passing_skill_value=stats.norm(loc=50, scale=20),
    ),
)


def _get_default_distribs():
    return DEFAULT_DISTRIBUTIONS


@attr.s(auto_attribs=True)
class AutoQuality:
    """This class implements a tool to help set up quality control for Toloka project.
    To use `toloka.autoquality` install toloka-kit via `pip install toloka-kit[autoquality]`

    Attributes:
        toloka_client: TolokaClient instance to interact with requester's account
        project_id: Toloka project ID
        base_pool_id: Template Pool for autoquality pools
        training_pool_id:  Training Pool ID
        exam_pool_id: Exam Pool ID
        exam_skill_id: Skill for filtering by exam perfomance
        label_field: Output field name
        n_iter: Number of an autoquality pools
        parameter_distributions: Parameter distributions
        score_func: Callable to calculate pool scores
        ranking_func: Callabale to ranking pools based on their scores
        create_autoquality_pool_func: Callable to create autoquality pool
        run_id: ID of autoquality run

    Example:
        >>> aq = AutoQuality(
        >>>   toloka_client=toloka_client,
        >>>   project_id=...,
        >>>   base_pool_id=...,
        >>>   training_pool_id=...,
        >>>   exam_pool_id = ...,
        >>>   exam_skill_id = ...
        >>> )
        >>> aq.setup_pools()
        >>> aq.create_tasks(aq_tasks)
        >>> aq.run()
        >>> aq.best_pool_params
    """
    toloka_client: TolokaClient
    project_id: str
    base_pool_id: str
    training_pool_id: str
    exam_pool_id: Optional[str] = None
    exam_skill_id: Optional[str] = None
    label_field: str = 'label'
    n_iter: int = 10
    parameter_distributions: Dict = attr.ib(factory=_get_default_distribs)
    score_func: Callable = default_calc_scores
    ranking_func: Callable = default_calc_ranks
    create_autoquality_pool_func: Callable = _create_autoquality_pool_default
    run_id: str = attr.attrib(
        init=False,
        default=f'AutoQuality Project {datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")}'
    )

    # internal fields
    autoquality_pools: List[Pool] = attr.attrib(init=False, factory=list)
    autoquality_pool_skills: Dict[str, Skill] = attr.attrib(init=False, factory=dict)
    worker_autoquality_pool_skills: Dict[str, str] = attr.attrib(init=False, factory=dict)
    params: Dict[str, Dict[str, Any]] = attr.attrib(init=False, factory=dict)
    _base_pool: Optional[Pool] = attr.attrib(init=False, default=None)
    _assigned_workers: Dict[str, str] = attr.attrib(init=False, factory=dict)
    _scores: Optional[Dict[str, Any]] = attr.attrib(init=False, default=None)
    _ranks: Optional[pd.DataFrame] = attr.attrib(init=False, default=None)
    _pruned_params: Optional[Dict[str, Dict[str, Any]]] = attr.attrib(init=False, default=None)

    def setup_pools(self):
        """Create autoquality pools with sampled quality control parameters.
        """
        logger.info('Creating pools')
        for params in ParameterSampler(
            self._params_to_flat_dict(self.parameter_distributions),
            self.n_iter * 10,
        ):
            if len(self.params) >= self.n_iter:
                break
            try:
                params = self._params_from_flat_dict(params)
                pool = self.create_autoquality_pool_func(
                    self,
                    params,
                    private_name=f'{self.run_id} params {len(self.autoquality_pools)}'
                )
                self.autoquality_pools.append(pool)
                self.params[pool.id] = params
                logger.info(params)
            except Exception as e:
                logger.error(f'Exception when initializing pool, params discarded: {e}')

        self._setup_pool_skill_filters()

    def create_tasks(self, tasks: List[Task]):
        """Add tasks to autoquality pools.
        If the GoldenSet rule is used in quality control then control tasks should also be provided.
        """
        logger.info('Creating tasks in pools')
        for pool in self.autoquality_pools:
            self._create_tasks(pool.id, tasks)

        logger.info('Setup complete, please verify')
        return

    def run(self):
        """Run autoquality process.
        """
        try:
            logger.info('Opening pools')
            self._open_pools()

            logger.info('Waiting for all pools to close')
            self._wait_pool_for_all_pools_to_close()
        except Exception as e:
            raise e
        finally:
            self._close_pools()

    @property
    def base_pool(self):
        if not self._base_pool:
            self._base_pool = self.toloka_client.get_pool(self.base_pool_id)
        return self._base_pool

    @property
    def scores(self):
        if self._scores is None:
            self._scores = self._calc_scores()
        return self._scores

    @property
    def ranks(self):
        if self._ranks is None:
            self._ranks = self._calc_ranks()
        return self._ranks

    @property
    def pruned_params(self):
        if self._pruned_params is None:
            self._pruned_params = self._calc_pruned_params()
        return self._pruned_params

    @property
    def best_pool_id(self):
        return self.ranks[self.ranks.main_rank == self.ranks.main_rank.max()].pool_id.item()

    @property
    def best_pool(self):
        for pool in self.autoquality_pools:
            if pool.id == self.best_pool_id:
                return pool

    @property
    def best_pool_params(self):
        return self.params[self.best_pool_id]

    @property
    def best_pruned_params(self):
        return self.pruned_params[self.best_pool_id]

    @staticmethod
    def _params_to_flat_dict(params):
        new_dict = {}
        for k, v in params.items():
            if isinstance(v, dict):
                nested_dict = AutoQuality._params_to_flat_dict(v)
                for param, val in nested_dict.items():
                    new_dict[f'{k}__{param}'] = val
            else:
                new_dict[k] = v
        return new_dict

    @staticmethod
    def _params_from_flat_dict(params):
        new_dict = {}
        for k, v in params.items():
            parts = k.split('__')
            if len(parts) > 1:
                nested_dict_key = parts[0]
                param_key = parts[1]
                if not new_dict.get(nested_dict_key):
                    new_dict[nested_dict_key] = {}
                new_dict[nested_dict_key][param_key] = v
            else:
                new_dict[k] = v
        return new_dict

    def _create_skill_if_not_exists(self, skill_name):
        skill = next(self.toloka_client.get_skills(name=skill_name), None)
        if skill:
            return skill
        return self.toloka_client.create_skill(
            name=skill_name,
            hidden=True,
        )

    def _create_tasks(self, pool_id: str, tasks_data: List[Task]):
        tasks = []
        for task in deepcopy(tasks_data):
            task.pool_id = pool_id
            tasks.append(task)
        self.toloka_client.create_tasks(tasks=tasks, allow_defaults=True)
        logger.info(f'Populated pool {pool_id} with {len(tasks)} tasks')

    def _setup_pool_skill_filters(self):
        for pool in self.autoquality_pools:
            pool_skill = self.autoquality_pool_skills[pool.id]
            pool.quality_control.add_action(
                collector=AnswerCount(),
                conditions=[AssignmentsAcceptedCount > 0],
                action=SetSkill(skill_id=pool_skill.id, skill_value=1),
            )
            for other_pool in self.autoquality_pools:
                if other_pool.id != pool.id:
                    pool.filter &= (Skill(self.autoquality_pool_skills[other_pool.id]) != 1)

            self.toloka_client.update_pool(pool.id, pool)

    def _open_pools(self):
        self.toloka_client.open_pool(self.training_pool_id)
        if self.exam_pool_id:
            self.toloka_client.open_pool(self.exam_pool_id)
        for i in range(len(self.autoquality_pools)):
            pool = self.toloka_client.get_pool(self.autoquality_pools[i].id)
            if pool.is_closed() and pool.last_close_reason == Pool.CloseReason.COMPLETED:
                continue
            self.autoquality_pools[i] = self.toloka_client.open_pool(self.autoquality_pools[i].id)

    def archive_autoquality_pools(self):
        """Archive all pools created by `AutoQuality.setup_pools`
        """
        for i in range(len(self.autoquality_pools)):
            self.autoquality_pools[i] = self.toloka_client.archive_pool(self.autoquality_pools[i].id)

    def _close_pools(self):
        self.toloka_client.close_pool(self.training_pool_id)
        if self.exam_pool_id:
            self.toloka_client.close_pool(self.exam_pool_id)
        for i in range(len(self.autoquality_pools)):
            self.autoquality_pools[i] = self.toloka_client.close_pool(self.autoquality_pools[i].id)

    def _assign_pool_skills(self, from_pool_id, pool_skills):
        pool_skills_copy = list(pool_skills)
        random.shuffle(pool_skills_copy)
        pool_skills_cycle = itertools.cycle(pool_skills_copy)
        df = self.toloka_client.get_assignments_df(from_pool_id,
                                                   field=[GetAssignmentsTsvParameters.Field.WORKER_ID],
                                                   exclude_banned=True)
        workers = df['ASSIGNMENT:worker_id'].unique()
        for worker_id in workers:
            if worker_id not in self.worker_autoquality_pool_skills:
                skill = next(pool_skills_cycle)
                self.toloka_client.set_user_skill(
                    skill_id=skill.id,
                    user_id=worker_id,
                    value=Decimal(1),
                )
                self.worker_autoquality_pool_skills[worker_id] = skill.id

    def _wait_pool_for_all_pools_to_close(self, minutes_to_wait=0.3):
        sleep_time = 60 * minutes_to_wait

        open_pools = self.autoquality_pools
        while open_pools:
            open_pools = []

            for pool in self.autoquality_pools:
                pool = self.toloka_client.get_pool(pool.id)
                if pool.is_open():
                    open_pools.append(pool)

            if open_pools:
                training_pool = self.toloka_client.get_pool(self.training_pool_id)
                if training_pool.is_open():
                    pool_skills = [self.autoquality_pool_skills[pool.id] for pool in open_pools]
                    self._assign_pool_skills(training_pool.id, pool_skills)

                time.sleep(sleep_time)

    def _calc_scores(self):
        scores = dict()
        for pool in self.autoquality_pools:
            score = None
            try:
                score = self.score_func(self.toloka_client, pool.id, self.label_field)
            except Exception as e:
                logger.error(f'Exception when computing pool scores, pool skipped: {e}')

            scores[pool.id] = dict(
                params=self.params[pool.id],
                score=score,
            )
        return scores

    def _calc_ranks(self):
        scores_df = pd.DataFrame([dict(pool_id=pool, **s['score'], **s['params']) for pool, s in self.scores.items() if
                                  s['score'] is not None])
        return self.ranking_func(scores_df)

    def _calc_pruned_params(self):
        pruned_params = dict()

        keep_params = ['ExamRequirement', 'TrainingRequirement', 'overlap']
        for pool_id, pool_score in self.scores.items():
            if not pool_score['score']:
                continue
            pruned_params[pool_id] = {param_name: param_config for param_name, param_config in
                                      pool_score['params'].items()
                                      if pool_score['score']['ban_reason_counts'].get(
                    param_name) or param_name in keep_params}
        return pruned_params
