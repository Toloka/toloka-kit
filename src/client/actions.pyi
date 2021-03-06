from enum import Enum
from typing import Any, Dict, Optional, overload

from .conditions import RuleConditionKey
from .user_restriction import DurationUnit, UserRestriction
from .util._codegen import BaseParameters


class RuleType(Enum):
    ...

class RuleAction(BaseParameters):

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(
        self,*,
        parameters: Optional[BaseParameters.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[BaseParameters.Parameters]

class Restriction(RuleAction):

    class Parameters(BaseParameters.Parameters):

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
            scope: Optional[UserRestriction.Scope] = ...,
            duration_days: Optional[int] = ...,
            private_comment: Optional[str] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        scope: Optional[UserRestriction.Scope]
        duration_days: Optional[int]
        private_comment: Optional[str]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        scope: Optional[UserRestriction.Scope] = ...,
        duration_days: Optional[int] = ...,
        private_comment: Optional[str] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class RestrictionV2(RuleAction):

    class Parameters(BaseParameters.Parameters):

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
            scope: Optional[UserRestriction.Scope] = ...,
            duration: Optional[int] = ...,
            duration_unit: Optional[DurationUnit] = ...,
            private_comment: Optional[str] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        scope: Optional[UserRestriction.Scope]
        duration: Optional[int]
        duration_unit: Optional[DurationUnit]
        private_comment: Optional[str]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        scope: Optional[UserRestriction.Scope] = ...,
        duration: Optional[int] = ...,
        duration_unit: Optional[DurationUnit] = ...,
        private_comment: Optional[str] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class SetSkillFromOutputField(RuleAction):

    class Parameters(BaseParameters.Parameters):

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
            skill_id: Optional[str] = ...,
            from_field: Optional[RuleConditionKey] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        skill_id: Optional[str]
        from_field: Optional[RuleConditionKey]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        skill_id: Optional[str] = ...,
        from_field: Optional[RuleConditionKey] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class ChangeOverlap(RuleAction):

    class Parameters(BaseParameters.Parameters):

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
            delta: Optional[int] = ...,
            open_pool: Optional[bool] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        delta: Optional[int]
        open_pool: Optional[bool]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        delta: Optional[int] = ...,
        open_pool: Optional[bool] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class SetSkill(RuleAction):

    class Parameters(BaseParameters.Parameters):

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
            skill_id: Optional[str] = ...,
            skill_value: Optional[int] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        skill_id: Optional[str]
        skill_value: Optional[int]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(
        self,*,
        skill_id: Optional[str] = ...,
        skill_value: Optional[int] = ...
    ) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class RejectAllAssignments(RuleAction):

    class Parameters(BaseParameters.Parameters):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(self, *, public_comment: Optional[str] = ...) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        public_comment: Optional[str]

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(self, *, public_comment: Optional[str] = ...) -> None: ...

    @overload
    def __init__(self, *, parameters: Optional[Parameters] = ...) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[Parameters]

class ApproveAllAssignments(RuleAction):

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(
        self,*,
        parameters: Optional[BaseParameters.Parameters] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    parameters: Optional[BaseParameters.Parameters]
