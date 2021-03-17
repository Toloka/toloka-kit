from typing import Any, Dict


class Solution(object):
    """Performer response for one task

    Attributes:
        output_values: Dictionary "field name" - "response value", by the number of fields that should be in the response.
    """

    def __repr__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, output_values: Dict[str, Any]) -> None: ...

    output_values: Dict[str, Any]
