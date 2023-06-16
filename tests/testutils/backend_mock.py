import attr
import logging
import operator

from typing import Any, Callable, Dict, List, Optional
from urllib.parse import urlparse, parse_qs

import httpx
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
    """Use in requests mock to imitate Toloka backend search methods.

    Attributes:
        storage: List of items. Imitates DB.
            Can be extended during tests to imitate new items appearance.
        limit: Default number of items to return in response.
    """

    storage: List[Any] = attr.ib(factory=list)
    limit: Optional[int] = attr.ib(default=None)
    responses: List[Dict[str, Any]] = attr.ib(factory=list, init=False)

    def __call__(self, request: httpx.Request) -> httpx.Response:
        params = request.url.params
        logger.info('Making request with params: %s', params)

        sort: List[str] = params.get_list('sort')
        params = params.remove('sort')
        limit: int = int(params.get('limit', str(self.limit)))
        params = params.remove('limit')

        conditions_exact = []
        conditions_interval = []
        for param in params:
            try:
                conditions_interval.append(ConditionInterval(param, params.get_list(param)))
            except Exception:
                conditions_exact.append(ConditionExact(param, params.get_list(param)))

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

        return httpx.Response(json=response, status_code=200)
