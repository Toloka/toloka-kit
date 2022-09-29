import inspect
import logging
from functools import lru_cache
from inspect import findsource
from stubmaker.builder.common import BaseDefinition


class GitHubSourceFinder:
    def __init__(self, source_root_url, handle_unknown_source='raise'):
        self.handle_unknown_source = handle_unknown_source
        self.source_root_url = source_root_url

    def __call__(self, definition: BaseDefinition):
        definition_module = inspect.getmodule(definition.obj)

        # handle package.__init__.py files
        if definition_module.__name__.split('.')[-1] != definition_module.__file__.split('/')[-1].replace('.py', ''):
            definition_module_name = definition.module_name + '.__init__'
        else:
            definition_module_name = definition.module_name

        file_path = '/'.join(definition_module_name.split('.')[1:]) + '.py'
        try:
            obj = definition.obj
            while hasattr(obj, '__wrapped__'):
                obj = obj.__wrapped__
            line = findsource(obj)[1]
        except OSError as exc:
            msg = f"Can't find source for {definition.obj}"
            if self.handle_unknown_source == 'ignore':
                logging.warning(msg)
                return None
            raise RuntimeError(msg) from exc
        return f'{self.source_root_url}/{file_path}#L{line}'
