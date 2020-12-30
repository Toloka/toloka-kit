from enum import Enum, unique
from typing import List

from ..primitives.base import attribute, BaseTolokaObject


class ViewSpec(BaseTolokaObject, spec_enum='Type', spec_field='type'):

    @unique
    class Type(Enum):
        CLASSIC = 'classic'
        TEMPLATE_BUILDER = 'tb'

    CLASSIC = Type.CLASSIC
    TEMPLATE_BUILDER = Type.TEMPLATE_BUILDER

    class Settings(BaseTolokaObject):
        show_finish: bool = attribute(origin='showFinish')
        show_fullscreen: bool = attribute(origin='showFullscreen')
        show_instructions: bool = attribute(origin='showInstructions')
        show_message: bool = attribute(origin='showMessage')
        show_reward: bool = attribute(origin='showReward')
        show_skip: bool = attribute(origin='showSkip')
        show_submit: bool = attribute(origin='showSubmit')
        show_timer: bool = attribute(origin='showTimer')
        show_title: bool = attribute(origin='showTitle')

    settings: Settings


class ClassicViewSpec(ViewSpec, spec_value=ViewSpec.CLASSIC):

    class Assets(BaseTolokaObject):
        script_urls: List[str]
        style_urls: List[str]

    script: str
    markup: str
    styles: str
    assets: Assets


class TemplateBuilderViewSpec(ViewSpec, spec_value=ViewSpec.TEMPLATE_BUILDER):
    pass
