from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .primitives.base import BaseTolokaObject
from .primitives.operators import (
    ComparableConditionMixin,
    CompareOperator,
    IdentityConditionMixin,
    IdentityOperator,
    InclusionConditionMixin,
    InclusionOperator,
    StatefulComparableConditionMixin
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

    def __or__(self, other: 'FilterCondition'): ...

    def __and__(self, other: 'FilterCondition'): ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self) -> None: ...

    _unexpected: Optional[Dict[str, Any]]

class FilterOr(FilterCondition):
    """Use to combine multiple filters via "or" logic

    Attributes:
        or_: list of filters to combine
    """

    def __or__(self, other: FilterCondition): ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, or_: List[FilterCondition]) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    or_: List[FilterCondition]

class FilterAnd(FilterCondition):
    """Use to combine multiple filters via "and" logic

    Attributes:
        and_: list of filters to combine
    """

    def __and__(self, other): ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, and_: List[FilterCondition]) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    and_: List[FilterCondition]

class Condition(FilterCondition):
    """Condition to select users.

    Attributes:
        operator: Comparison operator in the condition.
            For example, for a condition "The user must be 18 years old or older» used date of birth and operator
            GTE («Greater than or equal»). Possible key values operator depends on the data type in the field value
        value: Attribute value from the field key. For example, the ID of the region specified in the profile,
            or the minimum skill value.
    """

    class Category(Enum):
        ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, *, operator: Any, value: Any) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: Any
    value: Any

class Profile(Condition):
    """Use to select users based on profile data.

    Attributes:
        operator: Comparison operator in the condition.
        value: Attribute value from the field key.
    """

    class Key(Enum):
        """Possible criteria for filtering users by profile.
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

    def __init__(self, *, operator: Any, value: Any) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: Any
    value: Any

class Computed(Condition):
    """Use to select users based on data received or calculated by Toloka.

    Attributes:
        operator: Comparison operator in the condition.
        value: Attribute value from the field key.
    """

    class Key(Enum):
        """Possible criteria for filtering users by computed data.
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

    def __init__(self, *, operator: Any, value: Any) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: Any
    value: Any

class Skill(StatefulComparableConditionMixin, Condition):
    """Use to select users by skill value.

    To select users without a skill set the parameter value operator=CompareOperator.EQ and exclude the parameter value.
    Attributes:
        key: Skill ID.
        operator: Comparison operator in the condition.
        value: Attribute value from the field key.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __init__(
        self,
        key: str,
        operator: CompareOperator = ...,
        value: Optional[float] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    key: str
    operator: CompareOperator
    value: Optional[float]

class Gender(Profile, IdentityConditionMixin):
    """Use to select users by gender.

    Attributes:
        value: User gender.
    """

    class Gender(Enum):
        ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: IdentityOperator, value: Gender) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: Gender

class Country(Profile, IdentityConditionMixin):
    """Use to select users by country.

    Attributes:
        value: Country of the user (two-letter code of the standard ISO 3166-1 alpha-2).
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: IdentityOperator, value: str) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: str

class Citizenship(Profile, IdentityConditionMixin):
    """Use to select users by citizenship.

    Attributes:
        value: User citizenship (two-letter country code) ISO 3166-1 alpha-2
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: IdentityOperator, value: str) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: str

class Education(Profile, IdentityConditionMixin):
    """Use to select users by education.

    Attributes:
        value: User education.
    """

    class Education(Enum):
        """User education.
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

    def __init__(self, operator: IdentityOperator, value: Education) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: Education

class AdultAllowed(Profile, IdentityConditionMixin):
    """Use to select users by their agreement to perform tasks that contain adult content.

    Attributes:
        value: User agreement.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: IdentityOperator, value: bool) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: bool

class DateOfBirth(Profile, ComparableConditionMixin):
    """Use to select users by date of birth.

    Attributes:
        value: The user's date of birth (UNIX time in seconds).
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: CompareOperator, value: int) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: int

class City(Profile, InclusionConditionMixin):
    """Use to select users by city.

    Attributes:
        value: User city(ID of the region).
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: InclusionOperator, value: int) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: InclusionOperator
    value: int

class Languages(Profile, InclusionConditionMixin):
    """Use to select users by languages specified by the user in the profile.

    Attributes:
        value: Languages specified by the user in the profile (two-letter ISO code of the standard ISO 639-1 in upper case).
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
        self,
        operator: InclusionOperator,
        value: Union[str, List[str]]
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: InclusionOperator
    value: Union[str, List[str]]

class RegionByPhone(Computed, InclusionConditionMixin):
    """Use to select users by their region determined by the mobile phone number.

    Attributes:
        value: The user's region.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: InclusionOperator, value: int) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: InclusionOperator
    value: int

class RegionByIp(Computed, InclusionConditionMixin):
    """Use to select users by their region determined by IP address.

    Attributes:
        value: The user's region.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: InclusionOperator, value: int) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: InclusionOperator
    value: int

class DeviceCategory(Computed, IdentityConditionMixin):
    """Use to select users by their device category.

    Attributes:
        value: The user's device category.
    """

    class DeviceCategory(Enum):
        """Device сategory.
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

    def __init__(self, operator: IdentityOperator, value: DeviceCategory) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: DeviceCategory

class ClientType(Computed, IdentityConditionMixin):
    """Use to select users by their application type.

    Attributes:
        value: Client application type.
    """

    class ClientType(Enum):
        """Client application type.
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

    def __init__(self, operator: IdentityOperator, value: ClientType) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: ClientType

class OSFamily(Computed, IdentityConditionMixin):
    """Use to select users by their OS family.

    Attributes:
        value: The operating system family.
    """

    class OSFamily(Enum):
        """The operating system family.
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

    def __init__(self, operator: IdentityOperator, value: OSFamily) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: OSFamily

class OSVersion(Computed, ComparableConditionMixin):
    """Use to select users by OS full version.

    For example: 14.4
    Attributes:
        value: Full version of the operating system.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: CompareOperator, value: float) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: float

class OSVersionMajor(Computed, ComparableConditionMixin):
    """Use to select users by OS major version.

    For example: 14
    Attributes:
        value: Major version of the operating system.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: CompareOperator, value: int) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: int

class OSVersionMinor(Computed, ComparableConditionMixin):
    """Use to select users by OS minor version.

    For example: 4
    Attributes:
        value: Minor version of the operating system.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: CompareOperator, value: int) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: int

class OSVersionBugfix(Computed, ComparableConditionMixin):
    """Use to select users by build number (bugfix version) of the operating system.

    For example: 1
    Attributes:
        value: Build number (bugfix version) of the operating system.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, operator: CompareOperator, value: int) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: int

class UserAgentType(Computed, IdentityConditionMixin):
    """Use to select users by user agent type:

    Attributes:
        value: User agent type.
    """

    class UserAgentType(Enum):
        """User agent type.
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

    def __init__(self, operator: IdentityOperator, value: UserAgentType) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: UserAgentType

class UserAgentFamily(Computed, IdentityConditionMixin):
    """Use to select users by user agent family.

    Attributes:
        value: User agent family.
    """

    class UserAgentFamily(Enum):
        """User agent family.
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

    def __init__(self, operator: IdentityOperator, value: UserAgentFamily) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: IdentityOperator
    value: UserAgentFamily

class UserAgentVersion(Computed, ComparableConditionMixin):
    """Use to select users by full browser version.

    Attributes:
        value: Full browser version. <Major version>.<Minor version>.
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
        self,
        operator: CompareOperator,
        value: Optional[float] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: Optional[float]

class UserAgentVersionMajor(Computed, ComparableConditionMixin):
    """Use to select users by major browser version.

    Attributes:
        value: Major browser version.
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
        self,
        operator: CompareOperator,
        value: Optional[int] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: Optional[int]

class UserAgentVersionMinor(Computed, ComparableConditionMixin):
    """Use to select users by minor browser version.

    Attributes:
        value: Minor browser version.
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
        self,
        operator: CompareOperator,
        value: Optional[int] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: Optional[int]

class UserAgentVersionBugfix(Computed, ComparableConditionMixin):
    """Use to select users by build number (bugfix version) of the browser.

    Attributes:
        value: Build number (bugfix version) of the browser.
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
        self,
        operator: CompareOperator,
        value: Optional[int] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: Optional[int]

class Rating(Computed, ComparableConditionMixin):
    """Use to select users by user rating.

    Attributes:
        value: User rating. Calculated based on earnings in all projects available to the user.
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
        self,
        operator: CompareOperator,
        value: Optional[float] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    operator: CompareOperator
    value: Optional[float]
