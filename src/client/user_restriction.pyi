from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject


class DurationUnit(Enum):
    ...

class UserRestriction(BaseTolokaObject):
    """Allows you to control the performer's access to your projects and pools

    You can close user access to one or more projects. This allows you to control which users will perform tasks.
    For example, you can select users with a skill value below N and block them from accessing tasks.
    You can also unlock access.

    Attributes:
        user_id: Which performer is denied access.
        private_comment: A comment for you why access to this performer was restricted. 
        will_expire: When access is restored. If you do not set the parameter, then the access restriction is permanent.
        id: The identifier of a specific fact of access restriction. Read only.
        created: Date and time when the fact of access restriction was created. Read only.

    Example:
        How you can lock access for one user on one project.
        
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

    class Scope(Enum):
        """Restriction scope

        * ALL_PROJECTS - All the requester's projects.
        * PROJECT - A single project (specify the project_id).
        * POOL - A pool (specify the pool_id).
        """
        ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        user_id: Optional[str] = ...,
        private_comment: Optional[str] = ...,
        will_expire: Optional[datetime] = ...,
        id: Optional[str] = ...,
        created: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    user_id: Optional[str]
    private_comment: Optional[str]
    will_expire: Optional[datetime]
    id: Optional[str]
    created: Optional[datetime]

class AllProjectsUserRestriction(UserRestriction):
    """Forbid the performer from doing tasks from all your projects
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        user_id: Optional[str] = ...,
        private_comment: Optional[str] = ...,
        will_expire: Optional[datetime] = ...,
        id: Optional[str] = ...,
        created: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    user_id: Optional[str]
    private_comment: Optional[str]
    will_expire: Optional[datetime]
    id: Optional[str]
    created: Optional[datetime]

class PoolUserRestriction(UserRestriction):
    """Forbid the performer from doing tasks from a specific pool

    Attributes:
        pool_id: Pool identifier to which access will be denied.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        user_id: Optional[str] = ...,
        private_comment: Optional[str] = ...,
        will_expire: Optional[datetime] = ...,
        id: Optional[str] = ...,
        created: Optional[datetime] = ...,
        pool_id: Optional[str] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    user_id: Optional[str]
    private_comment: Optional[str]
    will_expire: Optional[datetime]
    id: Optional[str]
    created: Optional[datetime]
    pool_id: Optional[str]

class ProjectUserRestriction(UserRestriction):
    """Forbid the performer from doing tasks from a specific project

    Attributes:
        project_id: Project identifier to which access will be denied.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        user_id: Optional[str] = ...,
        private_comment: Optional[str] = ...,
        will_expire: Optional[datetime] = ...,
        id: Optional[str] = ...,
        created: Optional[datetime] = ...,
        project_id: Optional[str] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    user_id: Optional[str]
    private_comment: Optional[str]
    will_expire: Optional[datetime]
    id: Optional[str]
    created: Optional[datetime]
    project_id: Optional[str]

class SystemUserRestriction(UserRestriction):
    """DEPRECATED
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        user_id: Optional[str] = ...,
        private_comment: Optional[str] = ...,
        will_expire: Optional[datetime] = ...,
        id: Optional[str] = ...,
        created: Optional[datetime] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    user_id: Optional[str]
    private_comment: Optional[str]
    will_expire: Optional[datetime]
    id: Optional[str]
    created: Optional[datetime]
