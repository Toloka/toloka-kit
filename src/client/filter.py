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
]
import copy
import inspect
from enum import unique
from typing import Any, List, Optional, Union, ClassVar, Dict

from .primitives.base import BaseTolokaObject
from .primitives.operators import (
    CompareOperator,
    StatefulComparableConditionMixin,
    IdentityConditionMixin,
    ComparableConditionMixin,
    IdentityOperator,
    InclusionConditionMixin,
    InclusionOperator,
)
from ..util._codegen import attribute
from ..util._docstrings import inherit_docstrings
from ..util._extendable_enum import ExtendableStrEnum


class FilterCondition(BaseTolokaObject):
    """You can select Tolokers to access pool tasks.

    For example, you can select Tolokers by region, skill, or browser type (desktop or mobile).

    Example:
        How to setup filter for selecting Tolokers.

        >>> # you can combine filters using bitwise operators '|' and  '&'
        >>> filter = (
        >>>    (toloka.filter.Languages.in_('EN')) &
        >>>    (toloka.client.filter.DeviceCategory.in_(toloka.client.filter.DeviceCategory.SMARTPHONE))
        >>> )
        ...
    """

    def __or__(self, other: 'FilterCondition'):
        if isinstance(other, FilterOr):
            return other | self
        return FilterOr(or_=[self, other])

    def __and__(self, other: 'FilterCondition'):
        if isinstance(other, FilterAnd):
            return other & self
        return FilterAnd(and_=[self, other])

    def __invert__(self) -> 'FilterCondition':
        raise NotImplementedError('It is abstract method')

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

    def __invert__(self) -> 'FilterAnd':
        return FilterAnd(and_=[~condition for condition in self.or_])

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

    def __invert__(self) -> FilterOr:
        return FilterOr(or_=[~condition for condition in self.and_])

    def __iter__(self):
        return iter(self.and_)

    def __getitem__(self, item):
        return self.and_.__getitem__(item)

    @classmethod
    def structure(cls, data):
        return super(FilterCondition, cls).structure(data)


class Condition(FilterCondition, spec_field='category', spec_enum='Category'):
    """Condition to select Tolokers.

    Attributes:
        operator: Comparison operator in the condition.
            For example, for a condition "The Toloker must be 18 years old or older» used date of birth and operator
            GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value
        value: Attribute value from the field key. For example, the ID of the region specified in the profile,
            or the minimum skill value.
    """

    @unique
    class Category(ExtendableStrEnum):
        PROFILE = 'profile'
        COMPUTED = 'computed'
        SKILL = 'skill'

    operator: Any = attribute(required=True)
    value: Any = attribute(required=True)

    def __invert__(self) -> 'Condition':
        condition_copy = copy.deepcopy(self)
        condition_copy.operator = ~self.operator
        return condition_copy

    @classmethod
    def structure(cls, data):
        return super(FilterCondition, cls).structure(data)


@inherit_docstrings
class Profile(Condition, spec_value=Condition.Category.PROFILE, spec_field='key', spec_enum='Key'):
    """Use to select Tolokers based on profile data.
    """

    @unique
    class Key(ExtendableStrEnum):
        """Possible criteria for filtering Tolokers by profile.
        """

        GENDER = 'gender'
        COUNTRY = 'country'
        CITIZENSHIP = 'citizenship'
        EDUCATION = 'education'
        ADULT_ALLOWED = 'adult_allowed'
        DATE_OF_BIRTH = 'date_of_birth'
        CITY = 'city'
        LANGUAGES = 'languages'
        VERIFIED = 'verified'


@inherit_docstrings
class Computed(Condition, spec_value=Condition.Category.COMPUTED, spec_field='key', spec_enum='Key'):
    """Use to select Tolokers based on data received or calculated by Toloka.
    """

    @unique
    class Key(ExtendableStrEnum):
        """Possible criteria for filtering Tolokers by computed data.
        """

        CLIENT_TYPE = 'client_type'

        REGION_BY_PHONE = 'region_by_phone'
        REGION_BY_IP = 'region_by_ip'
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
    """Use to select Tolokers by skill value.

    To select Tolokers without a skill set the parameter value operator=CompareOperator.EQ and exclude the parameter value.
    Attributes:
        key: Skill ID.
        operator: Comparison operator in the condition.
        value: Attribute value from the field key.
    """

    key: str = attribute(required=True)
    operator: CompareOperator = attribute(default=CompareOperator.EQ, required=True)
    value: Optional[float] = attribute(default=None, required=True)


@inherit_docstrings
class Gender(Profile, IdentityConditionMixin, spec_value=Profile.Key.GENDER):
    """Use to select Tolokers by gender.

    Attributes:
        value: Toloker's gender.
    """

    @unique
    class Gender(ExtendableStrEnum):
        """Toloker's gender.
        """

        MALE = 'MALE'
        FEMALE = 'FEMALE'

    MALE = Gender.MALE
    FEMALE = Gender.FEMALE

    value: Gender = attribute(required=True, autocast=True)


@inherit_docstrings
class Country(Profile, IdentityConditionMixin, spec_value=Profile.Key.COUNTRY):
    """Use to select Tolokers by country.

    Attributes:
        value: Country of the Toloker (two-letter code of the standard ISO 3166-1 alpha-2).
    """

    value: str = attribute(required=True)  # ISO 3166-1 alpha-2


@inherit_docstrings
class Citizenship(Profile, IdentityConditionMixin, spec_value=Profile.Key.CITIZENSHIP):
    """Use to select Tolokers by citizenship.

    Attributes:
        value: Toloker's citizenship (two-letter country code) ISO 3166-1 alpha-2
    """

    value: str = attribute(required=True)  # ISO 3166-1 alpha-2


@inherit_docstrings
class Education(Profile, IdentityConditionMixin, spec_value=Profile.Key.EDUCATION):
    """Use to select Tolokers by education.

    Attributes:
        value: Toloker's education.
    """

    @unique
    class Education(ExtendableStrEnum):
        """Toloker's education.
        """

        BASIC = 'BASIC'
        MIDDLE = 'MIDDLE'
        HIGH = 'HIGH'

    BASIC = Education.BASIC
    MIDDLE = Education.MIDDLE
    HIGH = Education.HIGH

    value: Education = attribute(required=True, autocast=True)


@inherit_docstrings
class AdultAllowed(Profile, IdentityConditionMixin, spec_value=Profile.Key.ADULT_ALLOWED):
    """Use to select Tolokers by their agreement to perform tasks that contain adult content.

    Attributes:
        value: Toloker's agreement.

    Example:
        Use equal operator to create appropriate filter

        >>> adult_allowed_filter = toloka.client.filter.AdultAllowed == True
        >>> adult_not_allowed_filter = toloka.client.filter.AdultAllowed == False
        ...
    """

    value: bool = attribute(required=True)

    def __invert__(self) -> 'Condition':
        """Enforce to use `==` operator"""
        condition_copy = copy.deepcopy(self)
        if condition_copy.operator == IdentityOperator.NE:
            condition_copy.operator = IdentityOperator.EQ
        else:
            condition_copy.value = not condition_copy.value
        return condition_copy


@inherit_docstrings
class DateOfBirth(Profile, ComparableConditionMixin, spec_value=Profile.Key.DATE_OF_BIRTH):
    """Use to select Tolokers by date of birth.

    Attributes:
        value: The Toloker's date of birth (UNIX time in seconds).
    """

    value: int = attribute(required=True)


@inherit_docstrings
class City(Profile, InclusionConditionMixin, spec_value=Profile.Key.CITY):
    """Use to select Tolokers by city.

    Attributes:
        value: Toloker's city(ID of the region).
    """

    value: int = attribute(required=True)


@inherit_docstrings
class Languages(Profile, InclusionConditionMixin, spec_value=Profile.Key.LANGUAGES):
    """Use to select Tolokers by languages specified by the Toloker in the profile.

    Attributes:
        value: Language or list of languages specified by the Toloker in the profile
            (two-letter ISO code of the standard ISO 639-1 in upper case).
        verified: If set to True, only the Tolokers who have passed a language test will be selected. Currently, you can
            use this parameter only with the following ISO codes : `DE`, `EN`, `FR`, `JA`, `PT`, `SV`, `RU`, `AR`, `ES`,
            `HE`, `ID`, `ZH-HANS`.
    """

    VERIFIED_LANGUAGES_TO_SKILLS: ClassVar[Dict[str, str]] = {
        'AR': '30724',
        'DE': '26377',
        'EN': '26366',
        'ES': '32346',
        'FR': '26711',
        'HE': '44954',
        'ID': '39821',
        'JA': '26513',
        'PT': '26714',
        'RU': '26296',
        'SV': '29789',
        'ZH-HANS': '44742',
    }

    VERIFIED_LANGUAGE_SKILL_VALUE: ClassVar[int] = 100

    value: Union[str, List[str]] = attribute(required=True)

    def __new__(cls, *args, **kwargs):
        """Handle "verified" parameter

        If class is instantiated with `verified=True` parameter then return
        `FilterOr([
            FilterAnd([language_1, verified_skill_for_language_1]),
            ...
            FilterAnd([language_n, verified_skill_for_language_n])
        ])`
        condition for API compatibility reasons.
        """
        bound_args = inspect.signature(cls.__init__).bind(None, *args, **kwargs).arguments
        languages = bound_args['value']
        operator = bound_args['operator']
        verified = bound_args.pop('verified', False)

        if verified and operator == InclusionOperator.NOT_IN:
            raise ValueError('"Language not in" filter does not support verified=True argument')
        if verified and operator == InclusionOperator.IN:
            skills_mapping = cls.VERIFIED_LANGUAGES_TO_SKILLS
            try:
                if not isinstance(languages, list):
                    languages = [languages]
                result_conditions = FilterOr([])
                for language in languages:
                    verified_language_condition = (
                        Languages(operator=operator, value=language) &
                        Skill(skills_mapping[language]).eq(cls.VERIFIED_LANGUAGE_SKILL_VALUE)
                    )
                    result_conditions |= verified_language_condition

                return result_conditions
            except KeyError:
                if not isinstance(languages, str):
                    unsupported_languages = set(languages) - skills_mapping.keys()
                else:
                    unsupported_languages = [languages]
                raise ValueError(
                    'Following languages are not supported as verified languages:\n' + '\n'.join(unsupported_languages)
                )
        if isinstance(languages, list):
            if operator == InclusionOperator.IN:
                return FilterOr([Languages(operator=operator, value=language) for language in languages])
            else:
                return FilterAnd([Languages(operator=operator, value=language) for language in languages])
        return super().__new__(cls, *args, **kwargs)

    def __getnewargs__(self):
        """Due to redefined __new__ method class can't be deepcopied or pickled without __getnewargs__ definition"""
        return self.operator, self.value


# add fake parameter "verified: bool = False" to Languages.__init__ signature. This parameter will be consumed in
# Languages.__new__ while the actual __init__ is managed by attrs.
languages_init_signature = inspect.signature(Languages.__init__)
languages_init_signature_parameters = dict(languages_init_signature.parameters)
languages_init_signature_parameters['verified'] = inspect.Parameter(
    name='verified', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default=False, annotation=bool,
)
Languages.__init__.__annotations__['verified'] = bool
Languages.__init__.__signature__ = languages_init_signature.replace(parameters=languages_init_signature_parameters.values())


@inherit_docstrings
class Verified(Profile, IdentityConditionMixin, spec_value=Profile.Key.VERIFIED):
    """Use to select verified Tolokers.

    Attributes:
        value: is Toloker verified.

    Example:
        Use equal operator to create appropriate filter

        >>> verified_filter = toloka.client.filter.Verified == True
        >>> unverified_filter = toloka.client.filter.Verified == False
        ...
    """
    value: bool = attribute(required=True)

    def __invert__(self) -> 'Condition':
        """Enforce to use `==` operator"""
        condition_copy = copy.deepcopy(self)
        if condition_copy.operator == IdentityOperator.NE:
            condition_copy.operator = IdentityOperator.EQ
        else:
            condition_copy.value = not condition_copy.value
        return condition_copy


@inherit_docstrings
class RegionByPhone(Computed, InclusionConditionMixin, spec_value=Computed.Key.REGION_BY_PHONE):
    """Use to select Tolokers by their region determined by the mobile phone number.

    Attributes:
        value: The Toloker's region.
    """

    value: int = attribute(required=True)


@inherit_docstrings
class RegionByIp(Computed, InclusionConditionMixin, spec_value=Computed.Key.REGION_BY_IP):
    """Use to select Tolokers by their region determined by IP address.

    Attributes:
        value: The Toloker's region.
    """

    value: int = attribute(required=True)


@inherit_docstrings
class DeviceCategory(Computed, IdentityConditionMixin, spec_value=Computed.Key.DEVICE_CATEGORY):
    """Use to select Tolokers by their device category.

    Attributes:
        value: The Toloker's device category.
    """

    @unique
    class DeviceCategory(ExtendableStrEnum):
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

    value: DeviceCategory = attribute(required=True, autocast=True)


@inherit_docstrings
class ClientType(Computed, IdentityConditionMixin, spec_value=Computed.Key.CLIENT_TYPE):
    """Use to select Tolokers by their application type.

    Attributes:
        value: Client application type.
    """

    @unique
    class ClientType(ExtendableStrEnum):
        """Client application type.
        """

        BROWSER = 'BROWSER'
        TOLOKA_APP = 'TOLOKA_APP'

    value: ClientType = attribute(required=True, autocast=True)


@inherit_docstrings
class OSFamily(Computed, IdentityConditionMixin, spec_value=Computed.Key.OS_FAMILY):
    """Use to select Tolokers by their OS family.

    Attributes:
        value: The operating system family.
    """

    @unique
    class OSFamily(ExtendableStrEnum):
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

    value: OSFamily = attribute(required=True, autocast=True)


@inherit_docstrings
class OSVersion(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION):
    """Use to select Tolokers by OS full version.

    For example: 14.4
    Attributes:
        value: Full version of the operating system.
    """

    value: float = attribute(required=True)


@inherit_docstrings
class OSVersionMajor(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION_MAJOR):
    """Use to select Tolokers by OS major version.

    For example: 14
    Attributes:
        value: Major version of the operating system.
    """

    value: int = attribute(required=True)


@inherit_docstrings
class OSVersionMinor(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION_MINOR):
    """Use to select Tolokers by OS minor version.

    For example: 4
    Attributes:
        value: Minor version of the operating system.
    """

    value: int = attribute(required=True)


@inherit_docstrings
class OSVersionBugfix(Computed, ComparableConditionMixin, spec_value=Computed.Key.OS_VERSION_BUGFIX):
    """Use to select Tolokers by build number (bugfix version) of the operating system.

    For example: 1
    Attributes:
        value: Build number (bugfix version) of the operating system.
    """

    value: int = attribute(required=True)


@inherit_docstrings
class UserAgentType(Computed, IdentityConditionMixin, spec_value=Computed.Key.USER_AGENT_TYPE):
    """Use to select Tolokers by user agent type:

    Attributes:
        value: User agent type.
    """

    @unique
    class UserAgentType(ExtendableStrEnum):
        """User agent type.
        """

        BROWSER = 'BROWSER'
        MOBILE_BROWSER = 'MOBILE_BROWSER'
        OTHER = 'OTHER'

    BROWSER = UserAgentType.BROWSER
    MOBILE_BROWSER = UserAgentType.MOBILE_BROWSER
    OTHER = UserAgentType.OTHER

    value: UserAgentType = attribute(required=True, autocast=True)


@inherit_docstrings
class UserAgentFamily(Computed, IdentityConditionMixin, spec_value=Computed.Key.USER_AGENT_FAMILY):
    """Use to select Tolokers by user agent family.

    Attributes:
        value: User agent family.
    """

    @unique
    class UserAgentFamily(ExtendableStrEnum):
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

    value: UserAgentFamily = attribute(required=True, autocast=True)


@inherit_docstrings
class UserAgentVersion(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION):
    """Use to select Tolokers by full browser version.

    Attributes:
        value: Full browser version. <Major version>.<Minor version>.
    """

    value: float


@inherit_docstrings
class UserAgentVersionMajor(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION_MAJOR):
    """Use to select Tolokers by major browser version.

    Attributes:
        value: Major browser version.
    """

    value: int


@inherit_docstrings
class UserAgentVersionMinor(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION_MINOR):
    """Use to select Tolokers by minor browser version.

    Attributes:
        value: Minor browser version.
    """

    value: int


@inherit_docstrings
class UserAgentVersionBugfix(Computed, ComparableConditionMixin, spec_value=Computed.Key.USER_AGENT_VERSION_BUGFIX):
    """Use to select Tolokers by build number (bugfix version) of the browser.

    Attributes:
        value: Build number (bugfix version) of the browser.
    """

    value: int
