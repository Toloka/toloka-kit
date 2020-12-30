import datetime
from enum import unique, Enum

from .primitives.base import BaseTolokaObject


@unique
class DurationUnit(Enum):
    MINUTES = 'MINUTES'
    HOURS = 'HOURS'
    DAYS = 'DAYS'
    PERMANENT = 'PERMANENT'


class UserRestriction(BaseTolokaObject, spec_enum='Scope', spec_field='scope'):

    @unique
    class Scope(Enum):
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
    id: str
    created: datetime.datetime


class AllProjectsUserRestriction(UserRestriction, spec_value=UserRestriction.ALL_PROJECTS):
    pass


class PoolUserRestriction(UserRestriction, spec_value=UserRestriction.POOL):
    pool_id: str


class ProjectUserRestriction(UserRestriction, spec_value=UserRestriction.PROJECT):
    project_id: str


class SystemUserRestriction(UserRestriction, spec_value=UserRestriction.SYSTEM):
    pass
