from requests.models import Response
from typing import Any, List, Optional


class SpecClassIdentificationError(Exception):

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
        spec_field: Optional[str] = ...,
        spec_enum: Optional[str] = ...
    ) -> None: ...

    spec_field: Optional[str]
    spec_enum: Optional[str]

class ApiError(Exception):

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

    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class ValidationApiError(ApiError):

    _invalid_fields: Optional[List[str]]

class InternalApiError(ApiError):

    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class AuthenticationApiError(ApiError):

    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class AccessDeniedApiError(ApiError):

    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class RemoteServiceUnavailableApiError(ApiError):

    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class DoesNotExistApiError(ApiError):

    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class ConflictStateApiError(ApiError):

    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class TooManyRequestsApiError(ApiError):

    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

class IncorrectActionsApiError(ApiError):

    status_code: Optional[int]
    request_id: Optional[str]
    code: Optional[str]
    message: Optional[str]
    payload: Optional[Any]

def raise_on_api_error(response: Response): ...
