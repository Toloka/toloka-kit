__all__=['CloneResults']
from typing import NamedTuple, List

from .pool import Pool
from .project import Project
from .training import Training


class CloneResults(NamedTuple):
    """Objects created as a result of deep cloning of the project

    Attributes:
        project (Project): New project
        pools (List[Pool]): New pools. Can be empty.
        trainings (List[Training]): New trainings. Can be empty.
    """

    project: Project
    pools: List[Pool]
    trainings: List[Training]
