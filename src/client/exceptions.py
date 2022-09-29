__all__ = [
    'SpecClassIdentificationError',
    'ApiError',
    'ValidationApiError',
    'InternalApiError',
    'AuthenticationApiError',
    'AccessDeniedApiError',
    'RemoteServiceUnavailableApiError',
    'DoesNotExistApiError',
    'ConflictStateApiError',
    'TooManyRequestsApiError',
    'IncorrectActionsApiError',
    'raise_on_api_error',
    'FailedOperation',
]

import json
from typing import Optional, Any, List

import requests
import attr

from .error_codes import CommonErrorCodes, InternalErrorCodes
from ..util._docstrings import inherit_docstrings


# Client errors
@attr.attrs(auto_attribs=True, str=True, kw_only=True)
class SpecClassIdentificationError(Exception):
    """Raised when cannot find spec_сlass for spec_field value.

    Attributes:
        spec_field: value that defines spec_class type
        spec_enum: enum class containing spec_class possible types
    """

    spec_field: Optional[str] = None
    spec_enum: Optional[str] = None


@attr.attrs(auto_attribs=True, str=True, kw_only=True)
class FailedOperation(Exception):
    """Raised when an operation failed.

    Could be raised when an inner operation failed.

    Attributes:
        operation: Instance of failed operation.
    """
    operation: Optional[Any] = None


# API errors
@attr.attrs(auto_attribs=True, kw_only=True)
class ApiError(Exception):
    """Error returned from the API Call.

    Attributes:
        status_code: response status code.
        request_id: request ID
        code: error code string
        message: error message
        payload: additional payload
    """

    status_code: Optional[int] = None
    request_id: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None
    payload: Optional[Any] = None

    def __str__(self):
        head = f'You have got a(n) {type(self).__name__} with http status code: {self.status_code}'
        code = f'Code of error: {self.code}'
        error_details = f'Error details: {self.message}'
        if self.payload:
            additional_info = 'Additional information about the error:\n' + json.dumps(self.payload, indent=4)
        else:
            additional_info = ''
        request_id = f'request id: {self.request_id}. It needs to be specified when contacting support.'
        lines = [line for line in [head, code, error_details, additional_info, request_id] if line]
        result = '\n'.join(lines)
        return result


@inherit_docstrings
class ValidationApiError(ApiError):
    """Field validation error returned from the API Call.

    Attributes:
        invalid_fields: the list of the invalid fields
    """

    _invalid_fields: Optional[List[str]] = None

    @property
    def invalid_fields(self) -> List[str]:
        if self._invalid_fields is None:
            self._invalid_fields = list(self.payload.keys())

        return self._invalid_fields


@inherit_docstrings
class InternalApiError(ApiError):
    pass


@inherit_docstrings
class AuthenticationApiError(ApiError):
    pass


@inherit_docstrings
class AccessDeniedApiError(ApiError):
    pass


@inherit_docstrings
class RemoteServiceUnavailableApiError(ApiError):
    pass


@inherit_docstrings
class DoesNotExistApiError(ApiError):
    pass


@inherit_docstrings
class ConflictStateApiError(ApiError):
    pass


@inherit_docstrings
class TooManyRequestsApiError(ApiError):
    pass


@inherit_docstrings
class IncorrectActionsApiError(ApiError):
    pass


_ERROR_MAP = {
    CommonErrorCodes.VALIDATION_ERROR.value: ValidationApiError,
    CommonErrorCodes.INTERNAL_ERROR.value: InternalApiError,
    CommonErrorCodes.AUTHENTICATION_ERROR.value: AuthenticationApiError,
    CommonErrorCodes.ACCESS_DENIED.value: AccessDeniedApiError,
    CommonErrorCodes.DOES_NOT_EXIST.value: DoesNotExistApiError,
    CommonErrorCodes.CONFLICT_STATE.value: ConflictStateApiError,
    CommonErrorCodes.TOO_MANY_REQUESTS.value: TooManyRequestsApiError,
    CommonErrorCodes.REMOTE_SERVICE_UNAVAILABLE.value: RemoteServiceUnavailableApiError,
    **{code.value: IncorrectActionsApiError for code in InternalErrorCodes}
}


def raise_on_api_error(response: requests.Response):
    if 200 <= response.status_code < 300:
        return

    response_json = response.json()
    error_class = _ERROR_MAP.get(response_json['code'], ApiError)

    class_fields = [field.name for field in attr.fields(error_class)]
    for key in response_json.copy().keys():
        if key not in class_fields:
            response_json.pop(key)

    raise error_class(status_code=response.status_code, **response_json)
