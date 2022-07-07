import importlib.util
import os
import sys
import logging
import json
from argparse import ArgumentParser
from stubmaker.builder import override_module_import_path, traverse_modules

from ..builder.tk_representations_tree_builder import TolokaKitRepresentationTreeBuilder
from ..viewers.stub_viewer import TolokaKitStubViewer

from .. import constants


def make_stubs(
    module_root, src_root, output_dir, type_ignored_modules, skip_modules,
    modules_aliases_mapping, described_objects, broken_modules,
):
    # Making sure our module is imported from provided src-root even if
    # another version of the module is installed in the system
    override_module_import_path(module_root, src_root)

    for module_name, module in traverse_modules(module_root, src_root, skip_modules=skip_modules):

        # Normalizing paths before comparison and ensuring dst directory's existence
        dst_path = module.__file__.replace(src_root, output_dir) + 'i'
        dst_path = os.path.abspath(dst_path)
        src_path = os.path.abspath(module.__file__)
        assert src_path != dst_path, f'Attempting to override source file {module.__file__}'

        # Ensuring dst directory exists
        dst_dir = os.path.dirname(dst_path)
        os.makedirs(dst_dir, exist_ok=True)

        # Actually creating a file

        builder = TolokaKitRepresentationTreeBuilder(
            module_name, module, module_root,
            type_ignored_modules=type_ignored_modules,
            modules_aliases_mapping=modules_aliases_mapping,
            described_objects=described_objects,
        )
        viewer = TolokaKitStubViewer()

        with open(dst_path, 'w') as stub_flo:

            if module_name in broken_modules:
                logging.warning(f'Module {module_name} is known to be generated with errors! Please review output manually')
            logging.info(f'{module_name}: {src_path} => {dst_path}')
            module_view = viewer.view(builder.module_rep)
            stub_flo.write(module_view)


def main():
    parser = ArgumentParser()
    parser.add_argument('--module-root', type=str, required=True, help='Module name to import these sources as')
    parser.add_argument('--src-root', type=os.path.abspath, required=True, help='Path to source files to process')
    parser.add_argument('--output-dir', type=os.path.abspath, required=True)
    parser.add_argument(
        '--skip-modules', type=str, nargs='*', help='Module names to skip when generating stubs',
        default=constants.stubs.skip_modules
    )
    parser.add_argument('--type-ignored-modules', nargs='*', help='Module names to skip when generating stubs',
                        default=constants.stubs.type_ignored_modules)
    parser.add_argument(
        '--modules-aliases', type=os.path.abspath, required=False,
        help='Path to module names to aliases mapping in json format.',
    )
    parser.add_argument(
        '--described-objects', type=os.path.abspath, required=False,
        help='A dictionary from python objects to tuples consisting of module and qualname for each object (e.g. '
             "ModuleType: (types, ModuleType). Such objects' names and modules will not be deduced based on runtime "
             'data and provided names and modules will be used instead. Provided python file must have '
             'DESCRIBED_OBJECTS dictionary on the module level.'
    )
    parser.add_argument(
        '--logging-level', type=lambda x: str(x).upper(), required=False, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='WARNING'
    )
    args = parser.parse_args()

    logging.basicConfig(format='%(message)s', level=getattr(logging, args.logging_level), stream=sys.stderr)

    if args.described_objects:
        spec = importlib.util.spec_from_file_location(
            "described_objects", os.path.join(os.getcwd(), args.described_objects)
        )
        described_objects = importlib.util.module_from_spec(spec)
        sys.modules["described_objects"] = described_objects
        spec.loader.exec_module(described_objects)
        described_objects = getattr(described_objects, 'DESCRIBED_OBJECTS', None)
        if described_objects is None:
            raise RuntimeError('DESCRIBED_OBJECTS dict should be defined in python file specified in described-objects')

    make_stubs(
        module_root=args.module_root,
        src_root=args.src_root,
        output_dir=args.output_dir,
        type_ignored_modules=constants.stubs.type_ignored_modules,
        skip_modules=constants.stubs.skip_modules,
        modules_aliases_mapping=args.modules_aliases and json.load(open(args.modules_aliases)),
        described_objects=args.described_objects and described_objects,
        broken_modules=constants.stubs.broken_modules,
    )
