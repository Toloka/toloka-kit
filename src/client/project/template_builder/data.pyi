__all__ = [
    'BaseData',
    'InputData',
    'InternalData',
    'LocalData',
    'LocationData',
    'OutputData',
    'RelativeData',
]
import toloka.client.project.template_builder.base
import typing


class BaseDataMetaclass(toloka.client.project.template_builder.base.BaseTemplateMetaclass):
    @staticmethod
    def __new__(
        mcs,
        name,
        bases,
        namespace,
        **kwargs
    ): ...


class BaseData(toloka.client.project.template_builder.base.BaseComponent, metaclass=BaseDataMetaclass):
    """A base class for data components.

    For more information, see [Working with data](https://toloka.ai/docs/template-builder/operations/work-with-data).

     Attributes:
        path: A path to a data property in a component hierarchy.
            Dots are used as separators: `path.to.some.element`.
            For an array element, specify its sequence number after a dot: `items.0`.
        default: A default data value.
            Note, that it is shown in the interface, so it might hide placeholders, for example, in text fields.
    """

    def __init__(
        self,
        path: typing.Optional[typing.Any] = None,
        default: typing.Optional[typing.Any] = None
    ) -> None:
        """Method generated by attrs for class BaseData.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    path: typing.Optional[typing.Any]
    default: typing.Optional[typing.Any]


class InputData(BaseData):
    """Input data.

    For more information, see [Working with data](https://toloka.ai/docs/template-builder/operations/work-with-data).
    """

    def __init__(
        self,
        path: typing.Optional[typing.Any] = None,
        default: typing.Optional[typing.Any] = None
    ) -> None:
        """Method generated by attrs for class InputData.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    path: typing.Optional[typing.Any]
    default: typing.Optional[typing.Any]


class InternalData(BaseData):
    """Internal task data.

    Use it to store intermediate values.

    For more information, see [Working with data](https://toloka.ai/docs/template-builder/operations/work-with-data).
    """

    def __init__(
        self,
        path: typing.Optional[typing.Any] = None,
        default: typing.Optional[typing.Any] = None
    ) -> None:
        """Method generated by attrs for class InternalData.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    path: typing.Optional[typing.Any]
    default: typing.Optional[typing.Any]


class LocalData(BaseData):
    """Component data.

    It is used in some components, like [TransformHelperV1](toloka.client.project.template_builder.helpers.TransformHelperV1.md).

    For more information, see [Working with data](https://toloka.ai/docs/template-builder/operations/work-with-data).
    """

    def __init__(
        self,
        path: typing.Optional[typing.Any] = None,
        default: typing.Optional[typing.Any] = None
    ) -> None:
        """Method generated by attrs for class LocalData.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    path: typing.Optional[typing.Any]
    default: typing.Optional[typing.Any]


class LocationData(toloka.client.project.template_builder.base.BaseComponent):
    """Device coordinates.

    Use this component with the [DistanceConditionV1](toloka.client.project.template_builder.conditions.DistanceConditionV1.md) condition.

    For more information, see [data.location](https://toloka.ai/docs/template-builder/reference/data.location/).
    """

    def __init__(self) -> None:
        """Method generated by attrs for class LocationData.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]


class OutputData(BaseData):
    """Output data.

    For more information, see [Working with data](https://toloka.ai/docs/template-builder/operations/work-with-data).
    """

    def __init__(
        self,
        path: typing.Optional[typing.Any] = None,
        default: typing.Optional[typing.Any] = None
    ) -> None:
        """Method generated by attrs for class OutputData.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    path: typing.Optional[typing.Any]
    default: typing.Optional[typing.Any]


class RelativeData(BaseData):
    """A component for saving data in the [ListFieldV1](toloka.client.project.template_builder.fields.ListFieldV1).

    For more information, see [Working with data](https://toloka.ai/docs/template-builder/operations/work-with-data).
    """

    def __init__(
        self,
        path: typing.Optional[typing.Any] = None,
        default: typing.Optional[typing.Any] = None
    ) -> None:
        """Method generated by attrs for class RelativeData.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    path: typing.Optional[typing.Any]
    default: typing.Optional[typing.Any]
