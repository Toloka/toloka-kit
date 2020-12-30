from requests.models import Response
from typing import Any, Dict, List, Optional

from .primitives.base import BaseTolokaObject


class ApiError(BaseTolokaObject, Exception):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class ValidationApiError(ApiError):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...,
        invalid_fields: Optional[List[str]] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]
    _invalid_fields: Optional[List[str]]

class InternalApiError(ApiError):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class AuthenticationApiError(ApiError):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class AccessDeniedApiError(ApiError):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class RemoteServiceUnavailableApiError(ApiError):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class DoesNotExistApiError(ApiError):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class ConflictStateApiError(ApiError):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class TooManyRequestsApiError(ApiError):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class IncorrectActionsApiError(ApiError):

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
        status_code: Optional[int] = ...,
        request_id: Optional[str] = ...,
        code: Optional[str] = ...,
        message: Optional[str] = ...,
        payload: Optional[Any] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

def raise_on_api_error(response: Response): ...
