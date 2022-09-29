__all__ = [
    'BaseData',
    'InputData',
    'InternalData',
    'LocalData',
    'LocationData',
    'OutputData',
    'RelativeData',
]
from typing import Any

from .base import BaseComponent, ComponentType, base_component_or, BaseTemplateMetaclass
from ....util._codegen import attribute
from ....util._docstrings import inherit_docstrings


class BaseDataMetaclass(BaseTemplateMetaclass):
    def __new__(mcs, name, bases, namespace, **kwargs):

        if 'path' not in namespace:
            namespace['path'] = attribute()
            namespace.setdefault('__annotations__', {})['path'] = base_component_or(Any)
        if 'default' not in namespace:
            namespace['default'] = attribute()
            namespace.setdefault('__annotations__', {})['default'] = base_component_or(Any)

        return super().__new__(mcs, name, bases, namespace, **kwargs)


class BaseData(BaseComponent, metaclass=BaseDataMetaclass):
    """Components used for working with data: input, output, or intermediate.

     Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    pass


@inherit_docstrings
class InputData(BaseData, spec_value=ComponentType.DATA_INPUT):
    """The input data.

    For example, links to images that will be shown to Tolokers. In the Template Builder sandbox, you can
    set an example of input data.
    """

    pass


@inherit_docstrings
class InternalData(BaseData, spec_value=ComponentType.DATA_INTERNAL):
    """The data available only from within the task.

    This data is not saved to the results. Use this data to calculate or store intermediate values.
    """

    pass


@inherit_docstrings
class LocalData(BaseData, spec_value=ComponentType.DATA_LOCAL):
    """The local data available only from inside the component.

    This data is used in some auxiliary components, such as helper.transform.
    """

    pass


class LocationData(BaseComponent, spec_value=ComponentType.DATA_LOCATION):
    """This component sends the device coordinates

    To find out if the transmitted coordinates match the ones that you specified, use the conditions.DistanceConditionV1.
    """

    pass


@inherit_docstrings
class OutputData(BaseData, spec_value=ComponentType.DATA_OUTPUT):
    """The output data.

    This is what you get when you click the Send button.
    """

    pass


@inherit_docstrings
class RelativeData(BaseData, spec_value=ComponentType.DATA_RELATIVE):
    """A special component for saving data.

    It's only available in the field.list component.
    """

    pass
