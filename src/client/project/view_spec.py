import json
from copy import deepcopy
from enum import Enum, unique
from typing import List

from .template_builder import TemplateBuilder
from ..primitives.base import attribute, BaseTolokaObject
from ..util import traverse_dicts_recursively


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

    config: TemplateBuilder
    core_version: str = '1.0.0'

    def unstructure(self):
        data = super().unstructure()
        lock = {'core': data.pop('core_version')}

        for dct in traverse_dicts_recursively(data['config']):
            if 'type' not in dct or 'version' not in dct:
                continue

            comp_type = dct['type']
            if comp_type.startswith('data.'):
                continue

            comp_version = dct.pop('version')
            if comp_version != lock.setdefault(comp_type, comp_version):
                raise RuntimeError(f'Different versions of the same component: {comp_type}')

        data['lock'] = lock
        data['config'] = json.dumps(data['config'])
        return data

    @classmethod
    def structure(cls, data: dict):
        data_copy = deepcopy(data)
        lock = data_copy.pop('lock')

        data_copy['config'] = json.loads(data['config'])
        data_copy['core_version'] = lock['core']

        for dct in traverse_dicts_recursively(data_copy['config']):
            if dct.get('type') in lock:
                dct['version'] = lock[dct['type']]

        return super().structure(data_copy)
