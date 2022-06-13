__all__ = [
    'default_calc_scores',
    'default_calc_ranks'
]

import pandas as pd
import numpy as np

from collections import Counter
from crowdkit.aggregation import MajorityVote
from crowdkit.metrics.data import alpha_krippendorff, uncertainty
from scipy.stats import rankdata, bootstrap
from typing import Any, Dict

from ..client import TolokaClient, analytics_request
from ..client.assignment import GetAssignmentsTsvParameters


def default_calc_scores(toloka_client: TolokaClient, pool_id: str, label_field: str) -> Dict[str, Any]:
    """Calculate default scores for Autoquality.

    Args:
        toloka_client: `TolokaClient` instance to interact with requester's account
        pool_id: Pool ID to calculate scores for
        label_field: Target output field

    Returns:
        typing.Dict: Dict with scores
    """
    pool = toloka_client.get_pool(pool_id)
    answers_df = toloka_client.get_assignments_df(
        pool.id,
        field=[GetAssignmentsTsvParameters.Field.TASK_ID,
               GetAssignmentsTsvParameters.Field.WORKER_ID,
               GetAssignmentsTsvParameters.Field.SUBMITTED]
    )

    answers_df = answers_df.rename(columns={
        f'OUTPUT:{label_field}': 'label',
        GetAssignmentsTsvParameters.Field.WORKER_ID.value: 'worker',
        GetAssignmentsTsvParameters.Field.TASK_ID.value: 'task'
    })
    answers_df['ASSIGNMENT:submitted'] = answers_df['ASSIGNMENT:submitted'].apply(pd.to_datetime)
    answers_golden = answers_df[~answers_df[f'GOLDEN:{label_field}'].isnull()].copy()
    answers_golden['is_correct'] = answers_golden[f'GOLDEN:{label_field}'] == answers_golden['label']

    accuracies_golden_per_worker = answers_golden.groupby(['worker']).agg({'is_correct': np.mean})

    accuracy_golden = bootstrap((accuracies_golden_per_worker.reset_index()['is_correct'].values,),
                                statistic=np.mean).confidence_interval.low

    answers_df = answers_df[answers_df[f'GOLDEN:{label_field}'].isnull()]

    total_answered_tasks = len(answers_df['task'].unique())

    mv = MajorityVote()
    mv_labels = mv.fit_predict(answers_df)
    answers_df['mv_label'] = answers_df['task'].apply(lambda t: mv_labels[t])
    answers_df['mv_correct'] = answers_df['label'] == answers_df['mv_label']
    accuracies_mv_per_worker = answers_df.groupby(['worker']).agg({'mv_correct': np.mean})
    accuracy_mv = bootstrap((accuracies_mv_per_worker.reset_index()['mv_correct'].values,),
                            statistic=np.mean).confidence_interval.low

    uncertainty_score = uncertainty(answers=answers_df, workers_skills=mv.skills_)
    alpha_krippendorff_score = alpha_krippendorff(answers=answers_df)

    op = toloka_client.get_analytics([
        analytics_request.AvgSubmitAssignmentMillisPoolAnalytics(subject_id=pool.id),
        analytics_request.SpentBudgetPoolAnalytics(subject_id=pool.id),
        analytics_request.UniqueSubmittersCountPoolAnalytics(subject_id=pool.id),
    ])
    op = toloka_client.wait_operation(op)

    first_answer_dt = answers_df['ASSIGNMENT:submitted'].min()
    last_answer_dt = answers_df['ASSIGNMENT:submitted'].max()
    time_spent_seconds = (last_answer_dt - first_answer_dt).seconds

    restrictions = list(toloka_client.get_user_restrictions(
        scope='POOL', pool_id=pool.id,
    ))
    banned_users = {ban.user_id: ban.private_comment
                    for ban in restrictions if ban.user_id in answers_df['worker'].values}
    num_bans = len(banned_users.keys())
    ban_reason_counts = Counter(banned_users.values())

    scores = dict(
        accuracy_golden=accuracy_golden,
        accuracy_mv=accuracy_mv,
        alpha_krippendorff=alpha_krippendorff_score,
        uncertanity=uncertainty_score,
        time_spent_seconds=time_spent_seconds,
        unique_submitters_count=np.nan,
        spent_budget=np.nan,
        avg_submit_assignment_millis=np.nan,
        num_bans=num_bans,
        bans_ratio=np.nan,
        ban_reason_counts=ban_reason_counts
    )

    for analytics in op.details['value']:
        scores[analytics['request']['name']] = float(analytics['result'])

    scores['spent_budget'] = float(scores['spent_budget'])

    scores['spending_per_task'] = scores['spent_budget'] / total_answered_tasks
    scores['tasks_per_second'] = total_answered_tasks / scores['time_spent_seconds'] \
        if scores['time_spent_seconds'] else None
    scores['bans_ratio'] = num_bans / scores['unique_submitters_count'] if scores['unique_submitters_count'] else None
    return scores


def default_calc_ranks(scores_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate default pool ranks for autoquality

    Args:
        scores_df: pandas.DataFrame with `pool_id` column and columns with scores from `default_calc_scores`

    Returns:
        pandas.DataFrame: input DataFrame with an additional ranks columns

    """
    scores_df['accuracy_golden_rank'] = rankdata(scores_df['accuracy_golden'].round(2), method='dense')
    scores_df['accuracy_mv_rank'] = rankdata(scores_df['accuracy_mv'].round(2), method='dense')
    scores_df['alpha_krippendorff_rank'] = rankdata(scores_df['alpha_krippendorff'].round(2), method='dense')
    scores_df['spending_per_task_rank'] = rankdata(-1 * scores_df['spending_per_task'].round(2), method='dense')
    scores_df['tasks_per_second_rank'] = rankdata(scores_df['tasks_per_second'].round(3), method='dense')
    scores_df['bans_ratio_rank'] = rankdata(-1 * scores_df['bans_ratio'].round(3), method='dense')

    scores_df['avg_quality_rank'] = scores_df[
        ['accuracy_golden_rank', 'accuracy_mv_rank', 'alpha_krippendorff_rank']].mean(axis=1).round(2)
    scores_df['avg_rank'] = scores_df[
        ['avg_quality_rank', 'spending_per_task_rank', 'tasks_per_second_rank', 'bans_ratio_rank']].mean(axis=1)
    scores_df['optimal_quality_rank'] = (0.6 * scores_df['avg_quality_rank']
                                         + 0.4 * (2 / 6) * scores_df['bans_ratio_rank']
                                         + 0.4 * (3 / 6) * scores_df['spending_per_task_rank']
                                         + 0.4 * (1 / 6) * scores_df['tasks_per_second_rank'])
    scores_df['main_rank'] = scores_df['optimal_quality_rank']

    return scores_df
