from enum import Enum, unique
from typing import List, Any

from ...primitives.base import attribute

from .base import VersionedBaseComponent, BaseComponent, ComponentType, BaseTemplate, base_component_or


class BasePluginV1(VersionedBaseComponent):
    pass


class HotkeysPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_HOTKEYS):
    key_a: base_component_or(Any) = attribute(default=None, origin='a')
    key_b: base_component_or(Any) = attribute(default=None, origin='b')
    key_c: base_component_or(Any) = attribute(default=None, origin='c')
    key_d: base_component_or(Any) = attribute(default=None, origin='d')
    key_e: base_component_or(Any) = attribute(default=None, origin='e')
    key_f: base_component_or(Any) = attribute(default=None, origin='f')
    key_g: base_component_or(Any) = attribute(default=None, origin='g')
    key_h: base_component_or(Any) = attribute(default=None, origin='h')
    key_i: base_component_or(Any) = attribute(default=None, origin='i')
    key_j: base_component_or(Any) = attribute(default=None, origin='j')
    key_k: base_component_or(Any) = attribute(default=None, origin='k')
    key_l: base_component_or(Any) = attribute(default=None, origin='l')
    key_m: base_component_or(Any) = attribute(default=None, origin='m')
    key_n: base_component_or(Any) = attribute(default=None, origin='n')
    key_o: base_component_or(Any) = attribute(default=None, origin='o')
    key_p: base_component_or(Any) = attribute(default=None, origin='p')
    key_q: base_component_or(Any) = attribute(default=None, origin='q')
    key_r: base_component_or(Any) = attribute(default=None, origin='r')
    key_s: base_component_or(Any) = attribute(default=None, origin='s')
    key_t: base_component_or(Any) = attribute(default=None, origin='t')
    key_u: base_component_or(Any) = attribute(default=None, origin='u')
    key_v: base_component_or(Any) = attribute(default=None, origin='v')
    key_w: base_component_or(Any) = attribute(default=None, origin='w')
    key_x: base_component_or(Any) = attribute(default=None, origin='x')
    key_y: base_component_or(Any) = attribute(default=None, origin='y')
    key_z: base_component_or(Any) = attribute(default=None, origin='z')
    key_0: base_component_or(Any) = attribute(default=None, origin='0')
    key_1: base_component_or(Any) = attribute(default=None, origin='1')
    key_2: base_component_or(Any) = attribute(default=None, origin='2')
    key_3: base_component_or(Any) = attribute(default=None, origin='3')
    key_4: base_component_or(Any) = attribute(default=None, origin='4')
    key_5: base_component_or(Any) = attribute(default=None, origin='5')
    key_6: base_component_or(Any) = attribute(default=None, origin='6')
    key_7: base_component_or(Any) = attribute(default=None, origin='7')
    key_8: base_component_or(Any) = attribute(default=None, origin='8')
    key_9: base_component_or(Any) = attribute(default=None, origin='9')
    key_up: base_component_or(Any) = attribute(default=None, origin='up')
    key_down: base_component_or(Any) = attribute(default=None, origin='down')


class TriggerPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_TRIGGER):
    action: BaseComponent
    condition: BaseComponent
    fire_immediately: base_component_or(bool) = attribute(origin='fireImmediately')
    on_change_of: BaseComponent = attribute(origin='onChangeOf')


class TolokaPluginV1(BasePluginV1, spec_value=ComponentType.PLUGIN_TOLOKA):

    class TolokaPluginLayout(BaseTemplate):

        @unique
        class Kind(Enum):
            PAGER = 'pager'
            SCROLL = 'scroll'

        kind: Kind = Kind.SCROLL
        task_width: float = attribute(origin='taskWidth')

    layout: base_component_or(TolokaPluginLayout) = attribute(factory=TolokaPluginLayout)
    notifications: base_component_or(List[BaseComponent], 'ListBaseComponent')
