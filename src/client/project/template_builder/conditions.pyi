from typing import Any, Dict, List, Optional, Union

from .base import BaseComponent, VersionedBaseComponent


class BaseConditionV1(VersionedBaseComponent):
    """Check an expression against a condition.

    For example, you can check that a text field is filled in.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]

class AllConditionV1(BaseConditionV1):
    """Checks that all child conditions are met.

    If any of the conditions is not met, the component returns 'false'.

    If you only need one out of several conditions to be met, use the condition.any component. You can also combine
    these components.
    Attributes:
        conditions: A set of conditions that must be met.
        hint: Validation error message that the user will see.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...,
        conditions: Optional[Union[BaseComponent, List[BaseComponent]]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    conditions: Optional[Union[BaseComponent, List[BaseComponent]]]

class AnyConditionV1(BaseConditionV1):
    """Checks that at least one of the child conditions is met.

    If none of the conditions is met, the component returns false.

    If you need all conditions to be met, use the condition.all component. You can also combine these components.
    Attributes:
        conditions: A set of conditions, at least one of which must be met.
        hint: Validation error message that the user will see.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...,
        conditions: Optional[Union[BaseComponent, List[BaseComponent]]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    conditions: Optional[Union[BaseComponent, List[BaseComponent]]]

class EmptyConditionV1(BaseConditionV1):
    """Checks that the data is empty (undefined).

    Returns false if the data received a value.

    You can check:
        Template data (data.*).
        Data for the input field (field.*) that contains condition.empty.
    Attributes:
        data: Data to check. If not specified, data is checked in the component that contains condition.empty.
        hint: Validation error message that the user will see.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...,
        data: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    data: Optional[Any]

class EqualsConditionV1(BaseConditionV1):
    """Checks whether the original value is equal to the specified value.

    If it matches, it returns true, otherwise it returns false.

    When substituting values, you can refer to data.* or another element using $ref. You can also use helpers and
    conditions to get the value.
    Attributes:
        data: Original value. If not specified, it uses the value returned by the parent component (the component that
            contains condition.equals).
            How to pass a value:
                * Specify the value itself, like the number 42 or a string.
                * Get the value from your data.
                * Refer to another element using $ref.
                * Use helpers and conditions to get the value.
        hint: Validation error message that the user will see.
        to: The value to compare with the original.
            How to pass a value:
            * Specify the value itself, like the number 42 or a string.
            * Get the value from your data.
            * Refer to another element using $ref.
            * Use helpers and conditions to get the value.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...,
        to: Optional[Any] = ...,
        data: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    to: Optional[Any]
    data: Optional[Any]

class LinkOpenedConditionV1(BaseConditionV1):
    """Checks that the user clicked the link.

    Important: To trigger the condition, the user must follow the link from the Toloka interface — you must give users
    this option. The condition will not work if the user opens the link from the browser address bar.

    This condition can be used in the view.link component and also anywhere you can use (conditions).
    Attributes:
        hint: Validation error message that the user will see.
        url: The link that must be clicked.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...,
        url: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    url: Optional[Any]

class NotConditionV1(BaseConditionV1):
    """Returns the inverse of the specified condition.

    For example, if the specified condition is met (returns true), then condition.not will return false.
    Attributes:
        condition: The condition for which the inverse is returned.
        hint: Validation error message that the user will see.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...,
        condition: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    condition: Optional[BaseComponent]

class PlayedConditionV1(BaseConditionV1):
    """Checks the start of playback.

    Validation will be passed if playback is started. To play media with the condition.played check, you can use
    view.audio and view.video. The condition.played check only works in the player's validation property.
    Attributes:
        hint: Validation error message that the user will see.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]

class PlayedFullyConditionV1(BaseConditionV1):
    """This component checks for the end of playback.

    Validation is passed if playback is finished. To play media with the condition.played-fully check, you can use
    view.audio and view.video. The condition.played-fully check only works in the player's validation property.
    Attributes:
        hint: Validation error message that the user will see.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]

class RequiredConditionV1(BaseConditionV1):
    """Checks that the data is filled in. This way you can get the user to answer all the required questions.

    If used inside the validation property, you can omit the data property and the same property will be used from the
    parent component field (the one that contains the condition.required component).
    Attributes:
        data: Data to be filled in. If the property is not specified, the data of the parent component (the one that
            contains condition.required) is used.
        hint: Validation error message that the user will see.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...,
        data: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    data: Optional[Any]

class SchemaConditionV1(BaseConditionV1):
    """Allows validating data using JSON Schema. This is a special format for describing data in JSON format.

    For example, you can describe the data type, the minimum and maximum values, and specify that all values must be
    unique.

    This component is useful in the following cases:
        * If available components don't provide everything you need to configure validation.
        * If you already have a prepared JSON Schema configuration for the check and you want to use it.
    Attributes:
        data: Data that should be checked.
        hint: Validation error message that the user will see.
        schema: The schema for validating data.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...,
        data: Optional[Any] = ...,
        schema: Optional[Dict] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    data: Optional[Any]
    schema: Optional[Dict]

class SubArrayConditionV1(BaseConditionV1):
    """Checks that the array in data is a subarray for parent.

    Attributes:
        data: Subarray that is checked for in parent.
        hint: Validation error message that the user will see.
        parent: The array where data is searched for.
    """

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __setattr__(self, name, val): ...

    def __init__(
        self,*,
        version: Optional[str] = ...,
        hint: Optional[Any] = ...,
        data: Optional[Any] = ...,
        parent: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    hint: Optional[Any]
    data: Optional[Any]
    parent: Optional[Any]
