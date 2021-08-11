import attr
import logging
import operator

from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urlparse, parse_qs

from toloka.client import unstructure

logger = logging.getLogger(__name__)


@attr.s
class ConditionExact:
    field: str = attr.ib()
    value: List[str] = attr.ib(converter=frozenset, on_setattr=frozenset)

    def __call__(self, item: Dict[str, Any]) -> bool:
        return item.get(self.field) in self.value


@attr.s(init=False)
class ConditionInterval:

    COMPARATORS = {
        'gt': operator.gt,
        'lt': operator.lt,
        'gte': operator.ge,
        'lte': operator.le,
    }

    field: str = attr.ib()
    value: str = attr.ib()
    comparator: Callable[[str, str], bool] = attr.ib()

    def __init__(self, param: str, value: List[str]):
        self.field, suffix = param.rsplit('_', 1)
        self.comparator = self.COMPARATORS[suffix]
        if len(value) != 1:
            raise ValueError(f'Cant create interval condition for value: {value}')
        self.value = value[0]

    def __call__(self, item: Dict[str, Any]) -> bool:
        return self.comparator(item.get(self.field) or '', self.value)


@attr.s
class BackendSearchMock:
    """Use in requests mock to imitage Toloka backend search methods.

    Attributes:
        storage: List of items. Imitates DB.
            Can be extended during tests to imitate new items appearance.
        limit: Default number of items to return in response.
    """

    storage: List[Any] = attr.ib(factory=list)
    limit: Optional[int] = attr.ib(default=None)
    responses: List[Dict[str, Any]] = attr.ib(factory=list, init=False)

    def __call__(self, request: object, _: object) -> Dict[str, Any]:
        params: Dict[str, List[str]] = parse_qs(urlparse(request.url).query)
        logger.info('Making request with params: %s', params)

        sort: List[str] = params.pop('sort', [])
        limit: int = params.pop('limit', [self.limit])[0]

        conditions_exact = []
        conditions_interval = []
        for param, value in params.items():
            try:
                conditions_interval.append(ConditionInterval(param, value))
            except Exception:
                conditions_exact.append(ConditionExact(param, value))

        items = unstructure(list(self.storage))
        for field in reversed(sort):
            items.sort(reverse=field[0] == '-', key=lambda item: item.get(field.lstrip('-')) or '')

        for condition in conditions_exact + conditions_interval:
            items = list(filter(condition, items))

        logger.info('Items keeped: %d from %d', len(items), len(self.storage))
        items_limited = items[:int(limit)] if limit else items
        logger.info('Items limited: %d from %d', len(items_limited), len(items))

        response = {'items': items_limited,
                    'has_more': items_limited[-1] != items[-1] if items_limited else False}
        logger.info('Response: %s', response)
        self.responses.append(response)

        return response
