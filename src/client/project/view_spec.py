__all__ = [
    'ViewSpec',
    'ClassicViewSpec',
    'TemplateBuilderViewSpec'
]

import json

from copy import deepcopy
from enum import Enum, unique
from typing import List

from .template_builder import TemplateBuilder
from ..primitives.base import attribute, BaseTolokaObject
from ..util import traverse_dicts_recursively


class ViewSpec(BaseTolokaObject, spec_enum='Type', spec_field='type'):
    """Description of the task interface"""

    @unique
    class Type(Enum):
        """A view spec type

        Attributes:
            CLASSIC: A view defined with HTML, CSS and JS
            TEMPLATE_BUILDER: A view defined with template builder components
        """
        CLASSIC = 'classic'
        TEMPLATE_BUILDER = 'tb'

    CLASSIC = Type.CLASSIC
    TEMPLATE_BUILDER = Type.TEMPLATE_BUILDER

    class Settings(BaseTolokaObject):
        """ViewSpec Settings

        Attributes:
            show_finish: Show the Back to main page button.
            show_fullscreen: Show the Expand to fullscreen button.
            show_instructions: Show the Instructions button.
            show_message: Show the Message for the requester button.
            show_reward: Show the price per task page.
            show_skip: Show the Skip button.
            show_submit: Show the Next button.
            show_timer: Show the timer.
            show_title: Show the project name in task titles.
        """

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
    """A classic view specification defined with HTML, CSS and JS.
    For more information, see Toloka Requester's guide
    https://yandex.ru/support/toloka-requester/?lang=en

    Attributes:
        script: JavaScript interface for the task.
        markup: Task interface.
        styles: CSS task interface.
        asserts: Linked files such as:
            * CSS styles
            * JavaScript libraries
            * Toloka assets with the $TOLOKA_ASSETS prefix
            Add items in the order they should be linked when running the task interface.

    """

    class Assets(BaseTolokaObject):
        """
        style_urls: Links to CSS libraries.
        script_urls: Links to JavaScript libraries and Toloka assets.
            Toloka assets:
            * "$TOLOKA_ASSETS/js/toloka-handlebars-templates.js" — Handlebars. Ssee the description on the template
                engine website here http://handlebarsjs.com/
            * "$TOLOKA_ASSETS/js/image-annotation.js" — Image labeling interface. See image with area selection in
                the Requester's guide here https://yandex.ru/support/toloka-requester/concepts/t-components/image-annotation.html/?lang=en
            Note that the image labeling interface should only be connected together with the Handlebars helpers.
            The order of connection matters:
            >>> scipt_utls = [
            >>>     "$TOLOKA_ASSETS/js/toloka-handlebars-templates.js",
            >>>     "$TOLOKA_ASSETS/js/image-annotation.js",
            >>> ]
        """
        style_urls: List[str]
        script_urls: List[str]

    script: str
    markup: str
    styles: str
    assets: Assets


class TemplateBuilderViewSpec(ViewSpec, spec_value=ViewSpec.TEMPLATE_BUILDER):
    """A template builder view scpecification that defines an interface with
    template builder components

    Attributes:
        config: A template builder config
        core_version: Default template components version. Most users will not need to change this parameter.

    Example:
        How to declare simple interface:

        >>> import toloka.client.project.template_builder as tb
        >>> project_interface = toloka.project.view_spec.TemplateBuilderViewSpec(
        >>>     config=tb.TemplateBuilder(
        >>>         view=tb.view.ListViewV1(
        >>>             items=[header, output_field, radiobuttons],
        >>>             validation=some_validation,
        >>>         ),
        >>>         plugins=[plugin1, plugin2]
        >>>     )
        >>> )
        >>> # add 'project_interface' to 'toloka.project.Project' instance
        ...
    """

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
