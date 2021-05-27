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

    def _asdict(self):
        """Return a new dict which maps field names to their values.
        """
        ...

    _field_defaults = ...

    _fields = ...

    @classmethod
    def _make(cls, iterable):
        """Make a new CloneResults object from a sequence or iterable
        """
        ...

    def _replace(self, **kwds):
        """Return a new CloneResults object replacing specified fields with new values
        """
        ...

    project: Project
    pools: List[Pool]
    trainings: List[Training]
