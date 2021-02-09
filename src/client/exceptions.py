from typing import Optional, Any, List

import requests
import attr

from .error_codes import CommonErrorCodes, InternalErrorCodes


# Client errors
@attr.attrs(auto_attribs=True, str=True, kw_only=True)
class SpecClassIdentificationError(Exception):
    spec_field: Optional[str] = None
    spec_enum: Optional[str] = None


# API errors
@attr.attrs(auto_attribs=True, str=True, kw_only=True)
class ApiError(Exception):
    status_code: Optional[int] = None
    request_id: Optional[str] = None
    code: Optional[str] = None
    message: Optional[str] = None
    payload: Optional[Any] = None


class ValidationApiError(ApiError):

    _invalid_fields: Optional[List[str]] = None

    @property
    def invalid_fields(self) -> List[str]:
        if self._invalid_fields is None:
            self._invalid_fields = list(self.payload.keys())

        return self._invalid_fields


class InternalApiError(ApiError):
    pass


class AuthenticationApiError(ApiError):
    pass


class AccessDeniedApiError(ApiError):
    pass


class RemoteServiceUnavailableApiError(ApiError):
    pass


class DoesNotExistApiError(ApiError):
    pass


class ConflictStateApiError(ApiError):
    pass


class TooManyRequestsApiError(ApiError):
    pass


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
