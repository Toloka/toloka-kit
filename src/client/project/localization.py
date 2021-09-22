__all__ = [
    'AdditionalLanguage',
    'LocalizationConfig',
]
from enum import Enum, unique
from typing import List

from ..primitives.base import BaseTolokaObject
from ...util._codegen import attribute


class AdditionalLanguage(BaseTolokaObject):
    """Description for additional language in project

    Args:
        language: The language into which the translation is made. A string from ISO 639-1.
        public_name: Translation of the project field 'public_name' into the specified language.
        public_description: Translation of the project field 'public_description' into the specified language.
        public_instructions: Translation of the project field 'public_instructions' into the specified language.
    """

    class FieldTranslation(BaseTolokaObject):
        """Translation of one specific field

        Args:
            value: A string translated into the desired language.
            source: In creation you can pass only 'REQUESTER' right now.
        """

        @unique
        class Source(Enum):
            """Possible values of sources

            In creation you can pass only 'REQUESTER' right now.
            """
            REQUESTER = 'REQUESTER'

        value: str
        source: Source = attribute(factory=lambda: AdditionalLanguage.FieldTranslation.Source.REQUESTER,
                                   autocast=True)

    language: str
    public_name: FieldTranslation
    public_description: FieldTranslation
    public_instructions: FieldTranslation


class LocalizationConfig(BaseTolokaObject):
    """Translates the part of the project visible to the performers into different languages

    It is used to make it easier for performers from other countries who do not speak the necessary language to
    understand and perform tasks.

    Args:
        default_language: The source language used in the fields public_name, public_description, and public_instructions.
            Required parameter.
        additional_languages: List of translations into other languages. One element - one translation.
    """
    default_language: str
    additional_languages: List[AdditionalLanguage] = attribute(factory=list)
