__all__ = [
    'FilterCondition',
    'FilterOr',
    'FilterAnd',
    'Condition',
    'Profile',
    'Computed',
    'Skill',
    'Gender',
    'Country',
    'Citizenship',
    'Education',
    'AdultAllowed',
    'DateOfBirth',
    'City',
    'Languages',
    'RegionByPhone',
    'RegionByIp',
    'DeviceCategory',
    'ClientType',
    'OSFamily',
    'OSVersion',
    'OSVersionMajor',
    'OSVersionMinor',
    'OSVersionBugfix',
    'UserAgentType',
    'UserAgentFamily',
    'UserAgentVersion',
    'UserAgentVersionMajor',
    'UserAgentVersionMinor',
    'UserAgentVersionBugfix',
    'Rating'
]
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
    """You can select users to access pool tasks.

    For example, you can select users by region, skill, or browser type (desktop or mobile).

    Example:
        How to setup filter for selecting users.

        >>> # you can combine filters using bitwise operators '|' and  '&'
        >>> filter = (
        >>>    (toloka.filter.Languages.in_('EN')) &
        >>>    (toloka.client.filter.DeviceCategory.in_(toloka.client.filter.DeviceCategory.SMARTPHONE))
        >>> )
    """

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
    """Use to combine multiple filters via "or" logic

    Attributes:
        or_: list of filters to combine
    """

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
    """Use to combine multiple filters via "and" logic

    Attributes:
        and_: list of filters to combine
    """

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
    """Condition to select users.

    Attributes:
        operator: Comparison operator in the condition.
            For example, for a condition "The user must be 18 years old or older» used date of birth and operator
            GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value
        value: Attribute value from the field key. For example, the ID of the region specified in the profile,
            or the minimum skill value.
    """

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
    """Use to select users based on profile data.

    Attributes:
        operator: Comparison operator in the condition.
        value: Attribute value from the field key.
    """

    @unique
    class Key(Enum):
        """Possible criteria for filtering users by profile.
        """

        GENDER = 'gender'
        COUNTRY = 'country'
        CITIZENSHIP = 'citizenship'
        EDUCATION = 'education'
        ADULT_ALLOWED = 'adult_allowed'
        DATE_OF_BIRTH = 'date_of_birth'
        CITY = 'city'
        LANGUAGES = 'languages'


class Computed(Condition, spec_value=Condition.Category.COMPUTED, spec_field='key', spec_enum='Key'):
    """Use to select users based on data received or calculated by Toloka.

    Attributes:
        operator: Comparison operator in the condition.
        value: Attribute value from the field key.
    """

    @unique
    class Key(Enum):
        """Possible criteria for filtering users by computed data.
        """

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
    """Use to select users by skill value.

    To select users without a skill set the parameter value operator=CompareOperator.EQ and exclude the parameter value.
    Attributes:
        key: Skill ID.
        operator: Comparison operator in the condition.
        value: Attribute value from the field key.
    """

    key: str = attribute(required=True)
    operator: CompareOperator = attribute(default=CompareOperator.EQ, required=True)
    value: Optional[float] = attribute(default=None, required=True)


class Gender(Profile, IdentityConditionMixin, spec_value=Profile.Key.GENDER):
    """Use to select users by gender.

    Attributes:
        value: User gender.
    """

    @unique
    class Gender(Enum):
        """User gender.
        """

        MALE = 'MALE'
        FEMALE = 'FEMALE'

    MALE = Gender.MALE
    FEMALE = Gender.FEMALE

    value: Gender = attribute(required=True)


class Country(Profile, IdentityConditionMixin, spec_value=Profile.Key.COUNTRY):
    """Use to select users by country.

    Attributes:
        value: Country of the user (two-letter code of the standard ISO 3166-1 alpha-2).
    """

    value: str = attribute(required=True)  # ISO 3166-1 alpha-2


class Citizenship(Profile, IdentityConditionMixin, spec_value=Profile.Key.CITIZENSHIP):
    """Use to select users by citizenship.

    Attributes:
        value: User citizenship (two-letter country code) ISO 3166-1 alpha-2
    """

    value: str = attribute(required=True)  # ISO 3166-1 alpha-2


class Education(Profile, IdentityConditionMixin, spec_value=Profile.Key.EDUCATION):
    """Use to select users by education.

    Attributes:
        value: User education.
    """

    @unique
    class Education(Enum):
        """User education.
        """

        BASIC = 'BASIC'
        MIDDLE = 'MIDDLE'
        HIGH = 'HIGH'

    BASIC = Education.BASIC
    MIDDLE = Education.MIDDLE
    HIGH = Education.HIGH

    value: Education = attribute(required=True)


class AdultAllowed(Profile, IdentityConditionMixin, spec_value=Profile.Key.ADULT_ALLOWED):
    """Use to select users by their agreement to perform tasks that contain adult content.

    Attributes:
        value: User agreement.
    """

    value: bool = attribute(required=True)


class DateOfBirth(Profile, ComparableConditionMixin, spec_value=Profile.Key.DATE_OF_BIRTH):
    """Use to select users by date of birth.

    Attributes:
        value: The user's date of birth (UNIX time in seconds).
    """

    value: int = attribute(required=True)


class City(Profile, InclusionConditionMixin, spec_value=Profile.Key.CITY):
    """Use to select users by city.

    Attributes:
        value: User city(ID of the region).
    """

    value: int = attribute(required=True)


class Languages(Profile, InclusionConditionMixin, spec_value=Profile.Key.LANGUAGES):
    """Use to select users by languages specified by the user in the profile.

    Attributes:
        value: Languages specified by the user in the profile (two-letter ISO code of the standard ISO 639-1 in upper case).
    """

    value: Union[str, List[str]] = attribute(required=True)


class RegionByPhone(Computed, InclusionConditionMixin, spec_value=Computed.Key.REGION_BY_PHONE):
    """Use to select users by their region determined by the mobile phone number.

    Attributes:
        value: The user's region.
    """

    value: int = attribute(required=True)


class RegionByIp(Computed, InclusionConditionMixin, spec_value=Computed.Key.REGION_BY_IP):
    """Use to select users by their region determined by IP address.

    Attributes:
        value: The user's region.
    """

    value: int = attribute(required=True)


class DeviceCategory(Computed, IdentityConditionMixin, spec_value=Computed.Key.DEVICE_CATEGORY):
    """Use to select users by their device category.

    Attributes:
        value: The user's device category.
    """

    @unique
    class DeviceCategory(Enum):
        """Device сategory.
        """

        PERSONAL_COMPUTER = 'PERSONAL_COMPUTER'
        SMARTPHONE = 'SMARTPHONE'
        TABLET = 'TABLET'
        WEARABLE_COMPUTER = 'WEARABLE_COMPUTER'

    PERSONAL_COMPUTER = DeviceCategory.PERSONAL_COMPUTER
    SMARTPHONE = DeviceCategory.SMARTPHONE
    TABLET = DeviceCategory.TABLET
    WEARABLE_COMPUTER = DeviceCategory.WEARABLE_COMPUTER

    value: DeviceCategory = attribute(required=True)


class ClientType(Computed, IdentityConditionMixin, spec_value=Computed.Key.CLIENT_TYPE):
    """Use to select users by their application type.

    Attributes:
        value: Client application type.
    """

    @unique
    class ClientType(Enum):
        """Client application type.
        """

        BROWSER = 'BROWSER'
        TOLOKA_APP = 'TOLOKA_APP'

    value: ClientType = attribute(required=True)


class OSFamily(Computed, IdentityConditionMixin, spec_value=Computed.Key.OS_FAMILY):
    """Use to select users by their OS family.

    Attributes:
        value: The operating system family.
    """

    @unique
    class OSFamily(Enum):
        """The operating system family.
        """

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
    """Use to select users by OS full version.

    For example: 14.4
    Attributes:
        value: Full version of the operating system.
    """

    value: float = attribute(required=True)


class OSVersionMajor(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION_MAJOR):
    """Use to select users by OS major version.

    For example: 14
    Attributes:
        value: Major version of the operating system.
    """

    value: int = attribute(required=True)


class OSVersionMinor(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION_MINOR):
    """Use to select users by OS minor version.

    For example: 4
    Attributes:
        value: Minor version of the operating system.
    """

    value: int = attribute(required=True)


class OSVersionBugfix(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION_BUGFIX):
    """Use to select users by build number (bugfix version) of the operating system.

    For example: 1
    Attributes:
        value: Build number (bugfix version) of the operating system.
    """

    value: int = attribute(required=True)


class UserAgentType(Computed, IdentityConditionMixin, spec_value=Computed.Key.USER_AGENT_TYPE):
    """Use to select users by user agent type:

    Attributes:
        value: User agent type.
    """

    @unique
    class UserAgentType(Enum):
        """User agent type.
        """

        BROWSER = 'BROWSER'
        MOBILE_BROWSER = 'MOBILE_BROWSER'
        OTHER = 'OTHER'

    BROWSER = UserAgentType.BROWSER
    MOBILE_BROWSER = UserAgentType.MOBILE_BROWSER
    OTHER = UserAgentType.OTHER

    value: UserAgentType = attribute(required=True)


class UserAgentFamily(Computed, IdentityConditionMixin, spec_value=Computed.Key.USER_AGENT_FAMILY):
    """Use to select users by user agent family.

    Attributes:
        value: User agent family.
    """

    @unique
    class UserAgentFamily(Enum):
        """User agent family.
        """

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
    """Use to select users by full browser version.

    Attributes:
        value: Full browser version. <Major version>.<Minor version>.
    """

    value: float


class UserAgentVersionMajor(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION_MAJOR):
    """Use to select users by major browser version.

    Attributes:
        value: Major browser version.
    """

    value: int


class UserAgentVersionMinor(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION_MINOR):
    """Use to select users by minor browser version.

    Attributes:
        value: Minor browser version.
    """

    value: int


class UserAgentVersionBugfix(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION_BUGFIX):
    """Use to select users by build number (bugfix version) of the browser.

    Attributes:
        value: Build number (bugfix version) of the browser.
    """

    value: int


class Rating(Computed, ComparableConditionMixin, spec_value=Computed.Key.RATING):
    """Use to select users by user rating.

    Attributes:
        value: User rating. Calculated based on earnings in all projects available to the user.
    """

    value: float
