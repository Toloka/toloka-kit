from typing import NamedTuple, List

from .pool import Pool
from .project import Project
from .training import Training


class CloneResults(NamedTuple):
    project: Project
    pools: List[Pool]
    trainings: List[Training]
