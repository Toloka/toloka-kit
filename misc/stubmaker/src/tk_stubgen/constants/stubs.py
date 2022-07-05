skip_modules = [
    # Do not require stub generation
    'toloka.__version__',
]

# Modules that require "# type: ignore" during import
type_ignored_modules = [
    'jupyter_dash',
    'plotly',
    'kazoo',
    'dash',
]

# Modules that are known to generate incorrect stubs
broken_modules = {}
