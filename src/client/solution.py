from typing import Dict, Any

import attr


@attr.attrs(auto_attribs=True)
class Solution:
    output_values: Dict[str, Any]
