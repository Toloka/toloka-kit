__all__ = [
    'CloneResults',
]
import toloka.client.pool
import toloka.client.project
import toloka.client.training
import typing


class CloneResults(tuple):
    """Objects created as a result of deep cloning of the project

    Attributes:
        project (Project): New project
        pools (List[Pool]): New pools. Can be empty.
        trainings (List[Training]): New trainings. Can be empty.
    """

    project: toloka.client.project.Project
    pools: typing.List[toloka.client.pool.Pool]
    trainings: typing.List[toloka.client.training.Training]
