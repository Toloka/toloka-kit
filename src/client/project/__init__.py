__all__ = [
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
]

import datetime
from enum import Enum, unique

from ..primitives.base import BaseTolokaObject
from ..project.field_spec import (
    BooleanSpec,
    StringSpec,
    IntegerSpec,
    FloatSpec,
    UrlSpec,
    FileSpec,
    CoordinatesSpec,
    JsonSpec,
    ArrayBooleanSpec,
    ArrayStringSpec,
    ArrayIntegerSpec,
    ArrayFloatSpec,
    ArrayUrlSpec,
    ArrayFileSpec,
    ArrayCoordinatesSpec,
)
from ..project.view_spec import ClassicViewSpec, TemplateBuilderViewSpec
from ..project.task_spec import TaskSpec
from ..quality_control import QualityControl


class Project(BaseTolokaObject):
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
        >>>     assignments_issuing_type=toloka.project.Project.AssignmentsIssuingType.AUTOMATED,
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

    @unique
    class AssignmentsIssuingType(Enum):
        """How to assign tasks:

        Attributes:
            AUTOMATED: The user is assigned a task suite from the pool. You can configure the order
                for assigning task suites.
            MAP_SELECTOR: The user chooses a task suite on the map. If you are using MAP_SELECTOR,
            specify the text to display in the map by setting assignments_issuing_view_config.
        """

        AUTOMATED = 'AUTOMATED'
        MAP_SELECTOR = 'MAP_SELECTOR'

    @unique
    class ProjectStatus(Enum):
        """Project status:

        Attributes:
            ACTIVE: A project is active
            ARCHIVED: A project is archived
        """

        ACTIVE = 'ACTIVE'
        ARCHIVED = 'ARCHIVED'

    class AssignmentsIssuingViewConfig(BaseTolokaObject):
        """How the task will be displayed on the map

        Used only then assignments_issuing_type == MAP_SELECTOR

        Attributes:
            title_template: Name of the task. Users will see it in the task preview mode.
            description_template: Brief description of the task. Users will see it in the task preview mode.
        """

        title_template: str
        description_template: str

    QualityControl = QualityControl

    public_name: str  # public
    public_description: str  # public
    task_spec: TaskSpec  # public
    assignments_issuing_type: AssignmentsIssuingType  # AssignmentsIssuingType  # public

    assignments_issuing_view_config: AssignmentsIssuingViewConfig
    assignments_automerge_enabled: bool
    max_active_assignments_count: int
    quality_control: QualityControl

    # metadata: Dict[str, List[str]] ???
    status: ProjectStatus
    created: datetime.datetime

    id: str

    public_instructions: str  # public
    private_comment: str

    def __attrs_post_init__(self):
        # TODO: delegate this check to API
        if self.assignments_issuing_type == Project.AssignmentsIssuingType.MAP_SELECTOR:
            assert self.assignments_issuing_view_config is not None
