__all__ = [
    'field_spec',
    'task_spec',
    'template_builder',
    'view_spec',
    'Project',
    'ClassicViewSpec',
    'TemplateBuilderViewSpec',
    'BooleanSpec',
    'StringSpec',
    'IntegerSpec',
    'FloatSpec',
    'UrlSpec',
    'FileSpec',
    'CoordinatesSpec',
    'JsonSpec',
    'ArrayBooleanSpec',
    'ArrayStringSpec',
    'ArrayIntegerSpec',
    'ArrayFloatSpec',
    'ArrayUrlSpec',
    'ArrayFileSpec',
    'ArrayCoordinatesSpec',
    'LocalizationConfig',
    'AdditionalLanguage',
]
import datetime
import toloka.client.primitives.base
import toloka.client.project.localization
import toloka.client.project.task_spec
import toloka.client.quality_control
import toloka.util._extendable_enum
import typing

from toloka.client.project import (
    field_spec,
    task_spec,
    template_builder,
    view_spec
)
from toloka.client.project.field_spec import (
    ArrayBooleanSpec,
    ArrayCoordinatesSpec,
    ArrayFileSpec,
    ArrayFloatSpec,
    ArrayIntegerSpec,
    ArrayStringSpec,
    ArrayUrlSpec,
    BooleanSpec,
    CoordinatesSpec,
    FileSpec,
    FloatSpec,
    IntegerSpec,
    JsonSpec,
    StringSpec,
    UrlSpec
)
from toloka.client.project.localization import (
    AdditionalLanguage,
    LocalizationConfig
)
from toloka.client.project.view_spec import (
    ClassicViewSpec,
    TemplateBuilderViewSpec
)

class Project(toloka.client.primitives.base.BaseTolokaObject):
    """Top-level object in Toloka. All other entities are contained in some project.

    Describes one type of task from the requester's point of view. For example: one project can describe image segmentation,
    another project can test this segmentation. The easier the task, the better the results. If your task contains more
    than one question, it may be worth dividing it into several projects.

    In a project, you set properties for tasks and responses:
    * Input data parameters. These parameters describe the objects to display in a task, such as images or text.
    * Output data parameters. These parameters describe users' responses. They are used for validating the
        responses entered: the data type (integer, string, etc.), range of values, string length, and so on.
    * Task interface. For more information about how to define the appearance of tasks, see the document
        Toloka. requester's guide.

    Pools and training pools are related to a project.

    Attributes:
        public_name: Name of the project. Visible to users.
        public_description: Description of the project. Visible to users.
        public_instructions: Instructions for completing the task. You can use any HTML markup in the instructions.
        private_comment: Comments about the project. Visible only to the requester.
        task_spec: Parameters for input and output data and the task interface.
        assignments_issuing_type: How to assign tasks. The default value is AUTOMATED.
        assignments_automerge_enabled: Solve merging identical tasks in the project.
        max_active_assignments_count: The number of task suites the user can complete simultaneously (“Active” status)
        quality_control: The quality control rule.
        status: Project status.
        created: The UTC date and time the project was created.
        id: Project ID (assigned automatically).
        public_instructions: Instructions for completing tasks. You can use any HTML markup in the instructions.
        private_comment: Comment on the project. Available only to the customer.

    Example:
        How to create a new project.

        >>> toloka_client = toloka.TolokaClient(your_token, 'PRODUCTION')
        >>> new_project = toloka.project.Project(
        >>>     public_name='My best project!!!',
        >>>     public_description='Look at the instruction and do it well',
        >>>     public_instructions='!Describe your task for performers here!',
        >>>     task_spec=toloka.project.task_spec.TaskSpec(
        >>>         input_spec={'image': toloka.project.field_spec.UrlSpec()},
        >>>         output_spec={'result': toloka.project.field_spec.StringSpec(allowed_values=['OK', 'BAD'])},
        >>>         view_spec=verification_interface_prepared_before,
        >>>     ),
        >>> )
        >>> new_project = toloka_client.create_project(new_project)
        >>> print(new_project.id)
        ...
    """

    class AssignmentsIssuingType(toloka.util._extendable_enum.ExtendableStrEnum):
        """How to assign tasks:

        Attributes:
            AUTOMATED: The user is assigned a task suite from the pool. You can configure the order
                for assigning task suites.
            MAP_SELECTOR: The user chooses a task suite on the map. If you are using MAP_SELECTOR,
                specify the text to display in the map by setting assignments_issuing_view_config.
        """

        AUTOMATED = 'AUTOMATED'
        MAP_SELECTOR = 'MAP_SELECTOR'

    class ProjectStatus(toloka.util._extendable_enum.ExtendableStrEnum):
        """Project status:

        Attributes:
            ACTIVE: A project is active
            ARCHIVED: A project is archived
        """

        ACTIVE = 'ACTIVE'
        ARCHIVED = 'ARCHIVED'

    class AssignmentsIssuingViewConfig(toloka.client.primitives.base.BaseTolokaObject):
        """How the task will be displayed on the map

        Used only then assignments_issuing_type == MAP_SELECTOR

        Attributes:
            title_template: Name of the task. Users will see it in the task preview mode.
            description_template: Brief description of the task. Users will see it in the task preview mode.
        """

        def __init__(
            self,
            *,
            title_template: typing.Optional[str] = None,
            description_template: typing.Optional[str] = None
        ) -> None:
            """Method generated by attrs for class Project.AssignmentsIssuingViewConfig.
            """
            ...

        _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
        title_template: typing.Optional[str]
        description_template: typing.Optional[str]

    def set_default_language(self, language: str):
        """Sets the source language used in the fields public_name, public_description, and public_instructions.

        You must set the default language if you want to use the translation in the project to other languages.
        Args:
            language: The source language.
        """
        ...

    def add_requester_translation(
        self,
        language: str,
        public_name: typing.Optional[str] = None,
        public_description: typing.Optional[str] = None,
        public_instructions: typing.Optional[str] = None
    ):
        """Add new translations to other language.

        You can call it several times for different languages.
        If you call it for the same language, it overwrites new values, but don't overwrite values, that you don't pass.

        Args:
            language (str): Target language. A string from ISO 639-1.
            public_name (str): Translation of the project name.
            public_description (str): Translation of the project description.
            public_instructions (str): Translation of instructions for completing tasks.

        Examples:
            How to add russian translation to the project:

            >>> project = toloka.Project(
            >>>     public_name='cats vs dogs',
            >>>     public_description='image classification',
            >>>     public_instructions='do it pls',
            >>>     ...
            >>> )
            >>> project.set_default_language('EN')
            >>> project.add_requester_translation(
            >>>     language='RU',
            >>>     public_name='кошки против собак'
            >>>     public_description='классификация изображений'
            >>> )
            >>> project.add_requester_translation(language='RU', public_instructions='сделай это, пожалуйста')
        """
        ...

    def __init__(
        self,
        *,
        public_name: typing.Optional[str] = None,
        public_description: typing.Optional[str] = None,
        task_spec: typing.Optional[toloka.client.project.task_spec.TaskSpec] = None,
        assignments_issuing_type: typing.Union[AssignmentsIssuingType, str] = Project.AssignmentsIssuingType.AUTOMATED,
        assignments_issuing_view_config: typing.Optional[AssignmentsIssuingViewConfig] = None,
        assignments_automerge_enabled: typing.Optional[bool] = None,
        max_active_assignments_count: typing.Optional[int] = None,
        quality_control: typing.Optional[toloka.client.quality_control.QualityControl] = None,
        status: typing.Optional[ProjectStatus] = None,
        created: typing.Optional[datetime.datetime] = None,
        id: typing.Optional[str] = None,
        public_instructions: typing.Optional[str] = None,
        private_comment: typing.Optional[str] = None,
        localization_config: typing.Optional[toloka.client.project.localization.LocalizationConfig] = None
    ) -> None:
        """Method generated by attrs for class Project.
        """
        ...

    _unexpected: typing.Optional[typing.Dict[str, typing.Any]]
    public_name: typing.Optional[str]
    public_description: typing.Optional[str]
    task_spec: typing.Optional[toloka.client.project.task_spec.TaskSpec]
    assignments_issuing_type: AssignmentsIssuingType
    assignments_issuing_view_config: typing.Optional[AssignmentsIssuingViewConfig]
    assignments_automerge_enabled: typing.Optional[bool]
    max_active_assignments_count: typing.Optional[int]
    quality_control: typing.Optional[toloka.client.quality_control.QualityControl]
    status: typing.Optional[ProjectStatus]
    created: typing.Optional[datetime.datetime]
    id: typing.Optional[str]
    public_instructions: typing.Optional[str]
    private_comment: typing.Optional[str]
    localization_config: typing.Optional[toloka.client.project.localization.LocalizationConfig]
