from enum import Enum, unique
from typing import Any, List, Optional, Union

from .primitives.base import attribute, BaseTolokaObject
from .primitives.operators import (
    CompareOperator,
    StatefulComparableConditionMixin,
    IdentityConditionMixin,
    ComparableConditionMixin,
    InclusionConditionMixin,
)


class FilterCondition(BaseTolokaObject):

    def __or__(self, other: 'FilterCondition'):
        if isinstance(other, FilterOr):
            return other | self
        return FilterOr(or_=[self, other])

    def __and__(self, other: 'FilterCondition'):
        if isinstance(other, FilterAnd):
            return other & self
        return FilterAnd(and_=[self, other])

    @classmethod
    def structure(cls, data: dict):
        if 'or' in data:
            return FilterOr.structure(data)
        if 'and' in data:
            return FilterAnd.structure(data)
        else:
            return Condition.structure(data)


class FilterOr(FilterCondition, kw_only=False):
    or_: List[FilterCondition] = attribute(origin='or', required=True)

    def __or__(self, other: FilterCondition):
        self.or_.append(other)
        return self

    def __iter__(self):
        return iter(self.or_)

    def __getitem__(self, item):
        return self.or_.__getitem__(item)

    @classmethod
    def structure(cls, data):
        return super(FilterCondition, cls).structure(data)


class FilterAnd(FilterCondition, kw_only=False):
    and_: List[FilterCondition] = attribute(origin='and', required=True)

    def __and__(self, other):
        self.and_.append(other)
        return self

    def __iter__(self):
        return iter(self.and_)

    def __getitem__(self, item):
        return self.and_.__getitem__(item)

    @classmethod
    def structure(cls, data):
        return super(FilterCondition, cls).structure(data)


class Condition(FilterCondition, spec_field='category', spec_enum='Category'):

    @unique
    class Category(Enum):
        PROFILE = 'profile'
        COMPUTED = 'computed'
        SKILL = 'skill'

    operator: Any = attribute(required=True)
    value: Any = attribute(required=True)

    @classmethod
    def structure(cls, data):
        return super(FilterCondition, cls).structure(data)


class Profile(Condition, spec_value=Condition.Category.PROFILE, spec_field='key', spec_enum='Key'):

    @unique
    class Key(Enum):
        GENDER = 'gender'
        COUNTRY = 'country'
        CITIZENSHIP = 'citizenship'
        EDUCATION = 'education'
        ADULT_ALLOWED = 'adult_allowed'
        DATE_OF_BIRTH = 'date_of_birth'
        CITY = 'city'
        LANGUAGES = 'languages'


class Computed(Condition, spec_value=Condition.Category.COMPUTED, spec_field='key', spec_enum='Key'):

    @unique
    class Key(Enum):
        CLIENT_TYPE = 'client_type'

        REGION_BY_PHONE = 'region_by_phone'
        REGION_BY_IP = 'region_by_ip'
        RATING = 'rating'
        DEVICE_CATEGORY = 'device_category'
        OS_FAMILY = 'os_family'
        OS_VERSION = 'os_version'
        USER_AGENT_TYPE = 'user_agent_type'
        USER_AGENT_FAMILY = 'user_agent_family'
        USER_AGENT_VERSION = 'user_agent_version'

        OS_VERSION_MAJOR = 'os_version_major'
        OS_VERSION_MINOR = 'os_version_minor'
        OS_VERSION_BUGFIX = 'os_version_bugfix'
        USER_AGENT_VERSION_MAJOR = 'user_agent_version_major'
        USER_AGENT_VERSION_MINOR = 'user_agent_version_minor'
        USER_AGENT_VERSION_BUGFIX = 'user_agent_version_bugfix'


class Skill(StatefulComparableConditionMixin, Condition, order=False, eq=False, kw_only=False, spec_value=Condition.Category.SKILL):
    key: str = attribute(required=True)
    operator: CompareOperator = attribute(default=CompareOperator.EQ, required=True)
    value: Optional[float] = attribute(default=None, required=True)


class Gender(Profile, IdentityConditionMixin, spec_value=Profile.Key.GENDER):

    @unique
    class Gender(Enum):
        MALE = 'MALE'
        FEMALE = 'FEMALE'

    MALE = Gender.MALE
    FEMALE = Gender.FEMALE

    value: Gender = attribute(required=True)


class Country(Profile, IdentityConditionMixin, spec_value=Profile.Key.COUNTRY):
    value: str = attribute(required=True)  # ISO 3166-1 alpha-2


class Citizenship(Profile, IdentityConditionMixin, spec_value=Profile.Key.CITIZENSHIP):
    value: str = attribute(required=True)  # ISO 3166-1 alpha-2


class Education(Profile, IdentityConditionMixin, spec_value=Profile.Key.EDUCATION):

    @unique
    class Education(Enum):
        BASIC = 'BASIC'
        MIDDLE = 'MIDDLE'
        HIGH = 'HIGH'

    BASIC = Education.BASIC
    MIDDLE = Education.MIDDLE
    HIGH = Education.HIGH

    value: Education = attribute(required=True)


class AdultAllowed(Profile, IdentityConditionMixin, spec_value=Profile.Key.ADULT_ALLOWED):
    value: bool = attribute(required=True)


class DateOfBirth(Profile, ComparableConditionMixin, spec_value=Profile.Key.DATE_OF_BIRTH):
    value: int = attribute(required=True)


class City(Profile, InclusionConditionMixin, spec_value=Profile.Key.CITY):
    value: int = attribute(required=True)


class Languages(Profile, InclusionConditionMixin, spec_value=Profile.Key.LANGUAGES):
    value: Union[str, List[str]] = attribute(required=True)


class RegionByPhone(Computed, InclusionConditionMixin, spec_value=Computed.Key.REGION_BY_PHONE):
    value: int = attribute(required=True)


class RegionByIp(Computed, InclusionConditionMixin, spec_value=Computed.Key.REGION_BY_IP):
    value: int = attribute(required=True)


class DeviceCategory(Computed, IdentityConditionMixin, spec_value=Computed.Key.DEVICE_CATEGORY):

    @unique
    class DeviceCategory(Enum):
        PERSONAL_COMPUTER = 'PERSONAL_COMPUTER'
        SMARTPHONE = 'SMARTPHONE'
        TABLET = 'TABLET'

    PERSONAL_COMPUTER = DeviceCategory.PERSONAL_COMPUTER
    SMARTPHONE = DeviceCategory.SMARTPHONE
    TABLET = DeviceCategory.TABLET

    value: DeviceCategory = attribute(required=True)


class ClientType(Computed, IdentityConditionMixin, spec_value=Computed.Key.CLIENT_TYPE):

    @unique
    class ClientType(Enum):
        BROWSER = 'BROWSER'
        TOLOKA_APP = 'TOLOKA_APP'

    value: ClientType = attribute(required=True)


class OSFamily(Computed, IdentityConditionMixin, spec_value=Computed.Key.OS_FAMILY):

    @unique
    class OSFamily(Enum):
        WINDOWS = 'WINDOWS'
        OS_X = 'OS_X'
        MAC_OS = 'MAC_OS'
        LINUX = 'LINUX'
        BSD = 'BSD'
        ANDROID = 'ANDROID'
        IOS = 'IOS'
        BLACKBERRY = 'BLACKBERRY'

    WINDOWS = OSFamily.WINDOWS
    OS_X = OSFamily.OS_X
    MAC_OS = OSFamily.MAC_OS
    LINUX = OSFamily.LINUX
    BSD = OSFamily.BSD
    ANDROID = OSFamily.ANDROID
    IOS = OSFamily.IOS
    BLACKBERRY = OSFamily.BLACKBERRY

    value: OSFamily = attribute(required=True)


class OSVersion(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION):
    value: float = attribute(required=True)


class OSVersionMajor(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION_MAJOR):
    value: int = attribute(required=True)


class OSVersionMinor(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION_MINOR):
    value: int = attribute(required=True)


class OSVersionBugfix(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION_BUGFIX):
    value: int = attribute(required=True)


class UserAgentType(Computed, IdentityConditionMixin, spec_value=Computed.Key.USER_AGENT_TYPE):

    @unique
    class UserAgentType(Enum):
        BROWSER = 'BROWSER'
        MOBILE_BROWSER = 'MOBILE_BROWSER'
        OTHER = 'OTHER'

    BROWSER = UserAgentType.BROWSER
    MOBILE_BROWSER = UserAgentType.MOBILE_BROWSER
    OTHER = UserAgentType.OTHER

    value: UserAgentType = attribute(required=True)


class UserAgentFamily(Computed, IdentityConditionMixin, spec_value=Computed.Key.USER_AGENT_FAMILY):

    @unique
    class UserAgentFamily(Enum):
        IE = 'IE'
        CHROMIUM = 'CHROMIUM'
        CHROME = 'CHROME'
        FIREFOX = 'FIREFOX'
        SAFARI = 'SAFARI'
        YANDEX_BROWSER = 'YANDEX_BROWSER'

        IE_MOBILE = 'IE_MOBILE'
        CHROME_MOBILE = 'CHROME_MOBILE'
        MOBILE_FIREFOX = 'MOBILE_FIREFOX'
        MOBILE_SAFARI = 'MOBILE_SAFARI'

    IE = UserAgentFamily.IE
    CHROMIUM = UserAgentFamily.CHROMIUM
    CHROME = UserAgentFamily.CHROME
    FIREFOX = UserAgentFamily.FIREFOX
    SAFARI = UserAgentFamily.SAFARI
    YANDEX_BROWSER = UserAgentFamily.YANDEX_BROWSER

    IE_MOBILE = UserAgentFamily.IE_MOBILE
    CHROME_MOBILE = UserAgentFamily.CHROME_MOBILE
    MOBILE_FIREFOX = UserAgentFamily.MOBILE_FIREFOX
    MOBILE_SAFARI = UserAgentFamily.MOBILE_SAFARI

    value: UserAgentFamily = attribute(required=True)


class UserAgentVersion(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION):
    value: float


class UserAgentVersionMajor(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION_MAJOR):
    value: int


class UserAgentVersionMinor(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION_MINOR):
    value: int


class UserAgentVersionBugfix(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION_BUGFIX):
    value: int


class Rating(Computed, ComparableConditionMixin, spec_value=Computed.Key.RATING):
    value: float
