from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from .primitives.base import BaseTolokaObject


class DurationUnit(Enum):
    ...

class UserRestriction(BaseTolokaObject):

    class Scope(Enum):
        """Scope

        * ALL_PROJECTS — All the requester's projects.
        * PROJECT — A single project (specify the project_id).
        * POOL — A pool (specify the pool_id).
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
