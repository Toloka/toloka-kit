from enum import Enum, unique
from typing import List, Any

from .base import BaseTemplate, ComponentType, RefComponent, BaseComponent, VersionedBaseComponent, base_component_or


class BaseActionV1(VersionedBaseComponent):
    pass


class BulkActionV1(BaseActionV1, spec_value=ComponentType.ACTION_BULK):
    payload: base_component_or(List[BaseComponent], 'ListBaseComponent')


class NotifyActionV1(BaseActionV1, spec_value=ComponentType.ACTION_NOTIFY):

    class Payload(BaseTemplate):

        @unique
        class Theme(Enum):
            DANGER = 'danger'
            INFO = 'info'
            SUCCESS = 'success'
            WARNING = 'warning'

        content: base_component_or(Any)
        theme: base_component_or(Theme)
        delay: base_component_or(float)
        duration: base_component_or(float)

    payload: base_component_or(Payload)


class OpenCloseActionV1(BaseActionV1, spec_value=ComponentType.ACTION_OPEN_CLOSE):
    view: base_component_or(RefComponent)


class OpenLinkActionV1(BaseActionV1, spec_value=ComponentType.ACTION_OPEN_LINK):
    payload: base_component_or(Any)


class PlayPauseActionV1(BaseActionV1, spec_value=ComponentType.ACTION_PLAY_PAUSE):
    view: base_component_or(RefComponent)


class RotateActionV1(BaseActionV1, spec_value=ComponentType.ACTION_ROTATE):

    @unique
    class Payload(Enum):
        LEFT = 'left'
        RIGHT = 'right'

    payload: base_component_or(Payload)
    view: base_component_or(RefComponent)


class SetActionV1(BaseActionV1, spec_value=ComponentType.ACTION_SET):
    data: BaseComponent
    payload: base_component_or(Any)


class ToggleActionV1(BaseActionV1, spec_value=ComponentType.ACTION_TOGGLE):
    data: BaseComponent
