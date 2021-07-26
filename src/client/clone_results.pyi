__all__ = [
    'CloneResults',
]
from toloka.client.pool import Pool
from toloka.client.project import Project
from toloka.client.training import Training
from typing import List

class CloneResults(tuple):
    """Objects created as a result of deep cloning of the project

    Attributes:
        project (Project): New project
        pools (List[Pool]): New pools. Can be empty.
        trainings (List[Training]): New trainings. Can be empty.
    """

    project: Project
    pools: List[Pool]
    trainings: List[Training]
