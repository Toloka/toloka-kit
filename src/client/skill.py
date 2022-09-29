__all__ = ['Skill']
import datetime
from typing import Dict

from .owner import Owner
from .primitives.base import BaseTolokaObject
from ..util._codegen import attribute

LangIso639 = str


class Skill(BaseTolokaObject):
    """A skill is an assessment of some aspect of a Toloker's responses (a number from 0 to 100)

    Skill is a general grouping entity, for example "image annotation", which is created once and then used.
    To set the Skill value for a specific Toloker, use UserSkill.
    You can set up skill calculation in a quality control rule, or manually set the skill level for a Toloker.
    You can use skills to select Tolokers which are allowed to complete your tasks.

    Attributes:
        name: Skill name.
        private_comment: Comments on the skill (only visible to the requester).
        hidden: Access to information about the skill (the name and value) for Tolokers:
            * True - Closed. Default behavior.
            * False - Opened.
        skill_ttl_hours: The skill's "time to live" after the last update (in hours). The skill is removed from
            the Toloker's profile if the skill level hasn't been updated for the specified length of time.
        training: Whether the skill is related to a training pool:
            * True - The skill level is calculated from training pool tasks.
            * False - The skill isn't related to a training pool.
        public_name: Skill name for other Tolokers. You can provide a name in several languages (the message will come in the Toloker's language).
        public_requester_description: Skill description text for other Tolokers. You can provide text in several languages (the message will come in the Toloker's language).
        owner: Skill owner.
        id: Skill ID. Read only field.
        created: The UTC date and time when the skill was created. Read only field.

    Example:
        How to create new skill.

        >>> segmentation_skill = toloka_client.create_skill(
        >>>     name='Area selection of road signs',
        >>>     public_requester_description={
        >>>         'EN': 'Toloker annotates road signs',
        >>>         'RU': 'Как исполнитель размечает дорожные знаки',
        >>>     },
        >>> )
        >>> print(segmentation_skill.id)
        ...

        How to find skill.

        >>> segmentation_skill = next(toloka_client.get_skills(name='Area selection of road signs'), None)
        >>> if segmentation_skill:
        >>>     print(f'Segmentation skill already exists, with id {segmentation_skill.id}')
        >>> else:
        >>>     print('Create new segmentation skill here')
        ...
    """

    name: str

    private_comment: str
    hidden: bool
    skill_ttl_hours: int
    training: bool

    public_name: Dict[LangIso639, str]
    public_requester_description: Dict[LangIso639, str]
    owner: Owner

    # Readonly
    id: str = attribute(readonly=True)
    created: datetime.datetime = attribute(readonly=True)
