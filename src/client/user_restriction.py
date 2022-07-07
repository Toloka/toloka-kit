__all__ = [
    'DurationUnit',
    'UserRestriction',
    'AllProjectsUserRestriction',
    'PoolUserRestriction',
    'ProjectUserRestriction',
    'SystemUserRestriction'
]
import datetime
from enum import unique, Enum

from .primitives.base import BaseTolokaObject
from ..util._codegen import attribute
from ..util._docstrings import inherit_docstrings
from ..util._extendable_enum import ExtendableStrEnum


@unique
class DurationUnit(Enum):
    MINUTES = 'MINUTES'
    HOURS = 'HOURS'
    DAYS = 'DAYS'
    PERMANENT = 'PERMANENT'


class UserRestriction(BaseTolokaObject, spec_enum='Scope', spec_field='scope'):
    """Controls access to projects and pools.

    You can restrict access to any project for a Toloker. Then he can't do tasks in the project. You may set the duration of restriction or apply permanent restriction.
    To unlock access pass the restriction ID to the `delete_user_restriction`.

    Attributes:
        user_id: The ID of the Toloker.
        private_comment: A comment for you why access to this Toloker was restricted.
        will_expire: When access is restored. If you do not set the parameter, then the access restriction is permanent.
        id: The identifier of a specific fact of access restriction. Read only.
        created: Date and time when the fact of access restriction was created. Read only.

    Example:
        How you can lock access for one Toloker on one project.

        >>> new_restrict = toloka_client.set_user_restriction(
        >>>     ProjectUserRestriction(
        >>>         user_id='1',
        >>>         private_comment='I dont like you',
        >>>         project_id='5'
        >>>     )
        >>> )
        ...

        And how you can unlock it.

        >>> toloka_client.delete_user_restriction(new_restrict.id)
        ...
    """

    @unique
    class Scope(ExtendableStrEnum):
        """Restriction scope

        * ALL_PROJECTS - All the requester's projects.
        * PROJECT - A single project (specify the project_id).
        * POOL - A pool (specify the pool_id).
        """

        SYSTEM = 'SYSTEM'
        ALL_PROJECTS = 'ALL_PROJECTS'
        PROJECT = 'PROJECT'
        POOL = 'POOL'

    SYSTEM = Scope.SYSTEM
    ALL_PROJECTS = Scope.ALL_PROJECTS
    PROJECT = Scope.PROJECT
    POOL = Scope.POOL

    user_id: str
    private_comment: str
    will_expire: datetime.datetime

    # Readonly
    id: str = attribute(readonly=True)
    created: datetime.datetime = attribute(readonly=True)


@inherit_docstrings
class AllProjectsUserRestriction(UserRestriction, spec_value=UserRestriction.ALL_PROJECTS):
    """Forbid the Toloker to complete tasks from all your projects
    """

    pass


@inherit_docstrings
class PoolUserRestriction(UserRestriction, spec_value=UserRestriction.POOL):
    """Forbid the Toloker to complete tasks from a specific pool

    Attributes:
        pool_id: Pool identifier to which access will be denied.
    """

    pool_id: str


@inherit_docstrings
class ProjectUserRestriction(UserRestriction, spec_value=UserRestriction.PROJECT):
    """Forbid the Toloker to complete tasks from a specific project

    Attributes:
        project_id: Project identifier to which access will be denied.
    """

    project_id: str


@inherit_docstrings
class SystemUserRestriction(UserRestriction, spec_value=UserRestriction.SYSTEM):
    """DEPRECATED
    """

    pass
