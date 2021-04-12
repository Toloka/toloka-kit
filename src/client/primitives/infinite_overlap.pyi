from typing import Optional


class InfiniteOverlapParametersMixin(object):
    """
    This mixin provides `overlap` and `infinite_overlap` attributes
    and is responsible for maintaining their consistency.

    Possible states:
    * `overlap` is None and `infinite_overlap` is None:
        Interpreted as "overlap was not provided"
    * `overlap` is None and `infinite_overlap` is True:
        Interpreted as "infinite overlap"
    * `overlap` is not None and `infinite_overlap` is False:
        Interpreted as "finite overlap of `overlap`"

    All other states are considered invalid
    """

    def __attrs_post_init__(self): ...

    def unset_overlap(self):
        """Unsets overlap"""

        ...

    def unstructure(self) -> Optional[dict]: ...

    def __repr__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(self, infinite_overlap=..., overlap=...) -> None: ...

    _infinite_overlap: Optional[bool]
    _overlap: Optional[int]
