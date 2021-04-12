__all__ = ['Skill']
import datetime
from typing import Dict

from .primitives.base import BaseTolokaObject

LangIso639 = str


class Skill(BaseTolokaObject):
    """A skill is an assessment of some aspect of a user's responses (a number from 0 to 100)

    Skill is a general grouping entity, for example "image annotation", which is created once and then used.
    To set the Skill value for a specific performer, use UserSkill.
    You can set up skill calculation in a quality control rule, or manually set the skill level for a user.
    You can use skills to select users who perform pool tasks.

    Attributes:
        name: Skill name.
        private_comment: Comments on the skill (only visible to the requester).
        hidden: Access to information about the skill (the name and value) for users:
            * True - Closed. Default behaviour.
            * False - Opened.
        skill_ttl_hours: The skill's "time to live" after the last update (in hours). The skill is removed from
            the user's profile if the skill level hasn't been updated for the specified length of time.
        training: Whether the skill is related to a training pool:
            * True - The skill level is calculated from training pool tasks.
            * False - The skill isn't related to a training pool.
        public_name: Skill name for other users. You can provide a name in several languages (the message will come in the user's language).
        public_requester_description: Skill description text for other users. You can provide text in several languages (the message will come in the user's language).
        id: Skill ID. Read only field.
        created: The UTC date and time when the skill was created. Read only field.

    Example:
        How to create new skill.

        >>> segmentation_skill = toloka_client.create_skill(
        >>>     name='Area selection of road signs',
        >>>     public_requester_description={
        >>>         'EN': 'Performer is annotating road signs',
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

    # Readonly
    id: str
    created: datetime.datetime
