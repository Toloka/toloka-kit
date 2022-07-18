__all__ = ['Solution']
from typing import Dict, Any

import attr


@attr.attrs(auto_attribs=True)
class Solution:
    """Toloker's response for a task.

    Attributes:
        output_values: Dictionary "field name" - "response value", by the number of fields that should be in the response.
    """

    output_values: Dict[str, Any]
