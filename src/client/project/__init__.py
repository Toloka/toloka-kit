import datetime
from enum import Enum, unique

from ..primitives.base import BaseTolokaObject
from ..project.task_spec import TaskSpec
from ..quality_control import QualityControl


class Project(BaseTolokaObject):

    @unique
    class AssignmentsIssuingType(Enum):
        AUTOMATED = 'AUTOMATED'
        MAP_SELECTOR = 'MAP_SELECTOR'

    @unique
    class ProjectStatus(Enum):
        ACTIVE = 'ACTIVE'
        ARCHIVED = 'ARCHIVED'

    class AssignmentsIssuingViewConfig(BaseTolokaObject):
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
