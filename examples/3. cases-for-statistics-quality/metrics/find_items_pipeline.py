import collections
import datetime
import itertools
import logging
import os
import sys
from typing import List, Optional

import pandas as pd
import requests
from crowdkit.aggregation import BradleyTerry
from crowdkit.aggregation import MajorityVote
from toloka.client import Pool, Project, structure
from toloka.client import TolokaClient
from toloka.client.actions import ChangeOverlap
from toloka.client.collectors import AssignmentsAssessment
from toloka.client.conditions import AssessmentEvent
from toloka.client.exceptions import IncorrectActionsApiError
from toloka.client.task import Task
from toloka.streaming import AssignmentsObserver, Pipeline
from toloka.streaming.event import AssignmentEvent


logging.basicConfig(
    format='%(levelname)s - %(asctime)s - %(name)s: %(message)s',
    level=logging.INFO,
    stream=sys.stdout
)


GITHUB_RAW = 'https://raw.githubusercontent.com'
GITHUB_BASE_PATH = 'Toloka/toloka-kit/main/examples/6.streaming_pipelines'


class VerificationDoneHandler:
    """verification_pool -> find_items_pool back using quality control rule"""
    def __init__(self, client: TolokaClient, overlap_verification: int):
        self.client = client
        self.waiting = collections.defaultdict(list)
        self.overlap_verification = overlap_verification

    def __call__(self, events: List[AssignmentEvent]) -> None:
        for event in events:
            for task, solution in zip(event.assignment.tasks, event.assignment.solutions):
                answer = (solution.output_values['result'], event.assignment.user_id)
                self.waiting[task.input_values['assignment_id']].append(answer)

        to_aggregate = []
        for assignment_id, answers in self.waiting.items():
            if len(answers) >= self.overlap_verification:
                to_aggregate.extend((assignment_id, result, user_id) for result, user_id in answers)

        if to_aggregate:
            to_aggregate_df = pd.DataFrame(to_aggregate, columns=['task', 'label', 'performer'])
            aggregated = MajorityVote().fit_predict(to_aggregate_df)
            logging.info('Statuses to apply count: %s', collections.Counter(aggregated.values))

            for assignment_id, result in aggregated.items():
                try:
                    if result == 'Yes':
                        self.client.accept_assignment(assignment_id, 'Well done!')
                    else:
                        self.client.reject_assignment(assignment_id, 'Incorrect object.')
                except IncorrectActionsApiError:  # You could have accepted or rejected it in the UI.
                    logging.exception('Can\'t set status %s at %s', result, assignment_id)
                del self.waiting[assignment_id]

        logging.info('Waiting for verification count: %d', len(self.waiting))


class AcceptedItemsToComparison:
    """find_items_pool -> sbs_pool"""
    def __init__(self, client: TolokaClient, sbs_pool: Pool, overlap_find_items: int, overlap_sbs: int):
        self.client = client
        self.waiting = collections.defaultdict(list)
        self.sbs_pool = sbs_pool
        self.overlap_find_items = overlap_find_items
        self.overlap_sbs = overlap_sbs

    def __call__(self, events: List[AssignmentEvent]) -> None:
        for event in events:
            for task, solution in zip(event.assignment.tasks, event.assignment.solutions):
                self.waiting[task.input_values['image']].append(solution.output_values['found_link'])

        to_sbs = [(image, found_links)
                  for image, found_links in self.waiting.items()
                  if len(found_links) >= self.overlap_find_items]

        if to_sbs:
            logging.info('Got images ready for SbS count: %d', len(to_sbs))

            sbs_tasks = []
            for image, found_links in to_sbs:
                for left_link, right_link in itertools.combinations(found_links, 2):
                    input_values = {'image': image, 'left_link': left_link, 'right_link': right_link}
                    sbs_tasks.append(Task(pool_id=self.sbs_pool.id, overlap=self.overlap_sbs, input_values=input_values))

            logging.info('SbS tasks to create count: %d', len(sbs_tasks))
            self.client.create_tasks(sbs_tasks, open_pool=True)

        for image, _ in to_sbs:
            del self.waiting[image]
        logging.info('Waiting for SbS count: %d', len(self.waiting))


class HandleSbS:
    """sbs_pool results aggregation"""
    def __init__(self, client: TolokaClient, overlap_sbs: int):
        self.overlap_sbs = overlap_sbs
        self.client = client
        self.waiting = collections.defaultdict(list)
        self.scores_by_image = {}

    def __call__(self, events: List[AssignmentEvent]) -> None:
        for event in events:
            for task, solution in zip(event.assignment.tasks, event.assignment.solutions):
                answer = {'image': task.input_values['image'],
                          'performer': event.assignment.user_id,
                          'left': task.input_values['left_link'],
                          'right': task.input_values['right_link'],
                          'label': solution.output_values['result']}
                self.waiting[task.input_values['image']].append(answer)

        for image, answers in list(self.waiting.items()):
            if len(answers) >= self.overlap_sbs:
                scores = BradleyTerry(n_iter=100).fit_predict(pd.DataFrame(answers))
                self.scores_by_image[image] = scores.sort_values(ascending=False)
                del self.waiting[image]

        logging.info('Waiting for SbS aggregation count: %d', len(self.waiting))


class FoundItemsHandler:
    def __init__(self, client: TolokaClient, verification_pool: Pool, overlap_verification: int):
        self.overlap_verification = overlap_verification
        self.verification_pool = verification_pool
        self.client = client

    def __call__(self, events: List[AssignmentEvent]) -> None:
        verification_tasks = [
            Task(
                pool_id=self.verification_pool.id,
                unavailable_for=[event.assignment.user_id],
                overlap=self.overlap_verification,
                input_values={
                    'image': task.input_values['image'],
                    'found_link': solution.output_values['found_link'],
                    'assignment_id': event.assignment.id
                },
            )
            for event in events
            for task, solution in zip(event.assignment.tasks, event.assignment.solutions)
        ]
        self.client.create_tasks(verification_tasks, open_pool=True)
        logging.info('Verification tasks created count: %d', len(verification_tasks))


def _load_json_from_github(filename: str):
    response = requests.get(os.path.join(GITHUB_RAW, GITHUB_BASE_PATH, filename))
    response.raise_for_status()
    return response.json()


def create_project(client: TolokaClient, filename: str) -> Project:
    return client.create_project(_load_json_from_github(filename))


def create_pool(client: TolokaClient, filename: str, project_id: str, reward_per_assignment: float) -> Pool:
    pool = structure(_load_json_from_github(filename), Pool)
    pool.project_id = project_id
    pool.reward_per_assignment = reward_per_assignment
    pool.will_expire = datetime.datetime.now() + datetime.timedelta(days=3)
    return client.create_pool(pool)


class FindItemsPipeline:

    find_items_pool: Optional[Pool]
    verification_pool: Optional[Pool]
    sbs_pool: Optional[Pool]

    def __init__(
        self,
        client: TolokaClient,
        overlap_find_items=12, overlap_verification=3, overlap_sbs=3
    ):
        self.client = client
        self.overlap_find_items = overlap_find_items
        self.overlap_verification = overlap_verification
        self.overlap_sbs = overlap_sbs

        self.find_items_pool = None
        self.verification_pool = None
        self.sbs_pool = None

        self.pipeline = None

    def init_pipeline(self) -> None:
        find_items_project = create_project(self.client, 'find_items_project.json')
        find_items_pool = create_pool(self.client, 'find_items_pool.json', find_items_project.id, 0.08)
        verification_project = create_project(self.client, 'verification_project.json')
        verification_pool = create_pool(self.client, 'verification_pool.json', verification_project.id, 0.02)
        sbs_project = create_project(self.client, 'sbs_project.json')
        sbs_pool = create_pool(self.client, 'sbs_pool.json', sbs_project.id, 0.04)

        find_items_pool.quality_control.add_action(
            collector=AssignmentsAssessment(),
            conditions=[AssessmentEvent == AssessmentEvent.REJECT],
            action=ChangeOverlap(delta=1, open_pool=True),
        )
        self.client.update_pool(find_items_pool.id, find_items_pool)

        pipeline = Pipeline()
        found_items_observer = pipeline.register(AssignmentsObserver(self.client, find_items_pool.id))
        verification_observer = pipeline.register(AssignmentsObserver(self.client, verification_pool.id))
        sbs_observer = pipeline.register(AssignmentsObserver(self.client, sbs_pool.id))

        overlap_find_items = 12
        overlap_verification = 3
        overlap_sbs = 3

        found_items_observer.on_submitted(FoundItemsHandler(self.client, verification_pool, overlap_verification))
        found_items_observer.on_accepted(AcceptedItemsToComparison(self.client, sbs_pool, overlap_find_items, overlap_sbs))
        verification_observer.on_accepted(VerificationDoneHandler(self.client, overlap_verification))
        sbs_observer.on_accepted(HandleSbS(self.client, overlap_sbs))

        images = [
            'https://tlk.s3.yandex.net/wsdm2020/photos/8ca087fe33065d75327cafdb8720204b.jpg',
            'https://tlk.s3.yandex.net/wsdm2020/photos/d0c9eb8737f48df5964d93b08ec0d758.jpg',
            'https://tlk.s3.yandex.net/wsdm2020/photos/9245eed8aa1d1e6f5d5d39d00ab044c6.jpg',
            'https://tlk.s3.yandex.net/wsdm2020/photos/0aff4fc1edbe6096a9a517092902627f.jpg',
            'http://tolokaadmin.s3.yandex.net/demo/abb61898-c886-4e20-b7cd-c0d359ddbb9a',
        ]
        tasks = [
            Task(pool_id=find_items_pool.id, overlap=overlap_find_items, input_values={'image': image})
            for image in images
        ]
        self.client.create_tasks(tasks)

        self.find_items_pool = find_items_pool
        self.verification_pool = verification_pool
        self.sbs_pool = sbs_pool

        self.pipeline = pipeline

    def run(self):
        if self.pipeline is None:
            raise RuntimeError('You need to call FindItemsPipeline.init_pipeline before FindItemsPipeline.run')

        self.client.open_pool(self.find_items_pool.id)
        return self.pipeline.run()
