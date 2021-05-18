__all__ = [
    'BaseData',
    'InputData',
    'InternalData',
    'LocalData',
    'LocationData',
    'OutputData',
    'RelativeData'
]
from typing import Any

from .base import BaseComponent, ComponentType, base_component_or


class BaseData(BaseComponent):
    """Components used for working with data: input, output, or intermediate.

    """

    path: base_component_or(Any)
    default: base_component_or(Any)


class InputData(BaseData, spec_value=ComponentType.DATA_INPUT):
    """The input data.

    For example, links to images that will be shown to users. In the Template Builder sandbox, you can
    set an example of input data.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    pass


class InternalData(BaseData, spec_value=ComponentType.DATA_INTERNAL):
    """The data available only from within the task.

    This data is not saved to the results. Use this data to calculate or store intermediate values.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    pass


class LocalData(BaseData, spec_value=ComponentType.DATA_LOCAL):
    """The local data available only from inside the component.

    This data is used in some auxiliary components, such as helper.transform.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    pass


class LocationData(BaseComponent, spec_value=ComponentType.DATA_LOCATION):
    """This component sends the device coordinates

    To find out if the transmitted coordinates match the ones that you specified, use the conditions.DistanceConditionV1.
    """

    pass


class OutputData(BaseData, spec_value=ComponentType.DATA_OUTPUT):
    """The output data.

    This is what you get when you click the Send button.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    pass


class RelativeData(BaseData, spec_value=ComponentType.DATA_RELATIVE):
    """A special component for saving data.

    It's only available in the field.list component.
    Attributes:
        path: Path to the property containing data. Dots are used as separators: path.to.some.element. To specify the
            path to the array element, specify its sequence number starting from zero, for example: items.0
        default: The value to be used as the default data. This value will be shown in the interface, so it might hide
            some placeholders, for example, in the field.text component.
    """

    pass
