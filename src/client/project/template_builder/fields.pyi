from typing import Any, Dict, List, Optional, Union

from .base import (
    BaseComponent,
    BaseTemplate,
    ListDirection,
    ListSize,
    VersionedBaseComponent
)


class BaseFieldV1(VersionedBaseComponent):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]

class ButtonRadioFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        value_to_set: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    value_to_set: Optional[Any]

class GroupFieldOption(BaseTemplate):

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
        label: Optional[Any] = ...,
        value: Optional[Any] = ...,
        hint: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    label: Optional[Any]
    value: Optional[Any]
    hint: Optional[Any]

class ButtonRadioGroupFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]]

class CheckboxFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...,
        preserve_false: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    disabled: Optional[Union[BaseComponent, bool]]
    preserve_false: Optional[Union[BaseComponent, bool]]

class CheckboxGroupFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...,
        preserve_false: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]]
    disabled: Optional[Union[BaseComponent, bool]]
    preserve_false: Optional[Union[BaseComponent, bool]]

class DateFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        format: Optional[Any] = ...,
        block_list: Optional[Union[BaseComponent, List[Any]]] = ...,
        max: Optional[Any] = ...,
        min: Optional[Any] = ...,
        placeholder: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    format: Optional[Any]
    block_list: Optional[Union[BaseComponent, List[Any]]]
    max: Optional[Any]
    min: Optional[Any]
    placeholder: Optional[Any]

class ListFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        render: Optional[BaseComponent] = ...,
        button_label: Optional[Any] = ...,
        direction: Optional[Union[BaseComponent, ListDirection]] = ...,
        editable: Optional[Any] = ...,
        max_length: Optional[Union[BaseComponent, float]] = ...,
        size: Optional[Union[BaseComponent, ListSize]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    render: Optional[BaseComponent]
    button_label: Optional[Any]
    direction: Optional[Union[BaseComponent, ListDirection]]
    editable: Optional[Any]
    max_length: Optional[Union[BaseComponent, float]]
    size: Optional[Union[BaseComponent, ListSize]]

class NumberFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        maximum: Optional[Union[BaseComponent, int]] = ...,
        minimum: Optional[Union[BaseComponent, int]] = ...,
        placeholder: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    maximum: Optional[Union[BaseComponent, int]]
    minimum: Optional[Union[BaseComponent, int]]
    placeholder: Optional[Any]

class RadioGroupFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    options: Optional[Union[BaseComponent, List[Union[BaseComponent, GroupFieldOption]]]]
    disabled: Optional[Union[BaseComponent, bool]]

class SelectFieldV1(BaseFieldV1):

    class Option(BaseTemplate):

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
            label: Optional[Any] = ...,
            value: Optional[Any] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        label: Optional[Any]
        value: Optional[Any]

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        options: Optional[Union[BaseComponent, Option]] = ...,
        placeholder: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    options: Optional[Union[BaseComponent, Option]]
    placeholder: Optional[Any]

class TextFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...,
        placeholder: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    disabled: Optional[Union[BaseComponent, bool]]
    placeholder: Optional[Any]

class TextareaFieldV1(BaseFieldV1):

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
        data: Optional[BaseComponent] = ...,
        hint: Optional[Any] = ...,
        label: Optional[Any] = ...,
        validation: Optional[BaseComponent] = ...,
        disabled: Optional[Union[BaseComponent, bool]] = ...,
        placeholder: Optional[Any] = ...,
        resizable: Optional[Union[BaseComponent, bool]] = ...,
        rows: Optional[Union[BaseComponent, float]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    version: Optional[str]
    data: Optional[BaseComponent]
    hint: Optional[Any]
    label: Optional[Any]
    validation: Optional[BaseComponent]
    disabled: Optional[Union[BaseComponent, bool]]
    placeholder: Optional[Any]
    resizable: Optional[Union[BaseComponent, bool]]
    rows: Optional[Union[BaseComponent, float]]
