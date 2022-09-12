# pyyaml is required

import argparse
import yaml
from pathlib import Path


class IndentListDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path)
    args = parser.parse_args()
    with open(args.path) as f:
        parsed = yaml.load(f, Loader=yaml.SafeLoader)
        parsed["items"].append(
            {"name": "Python SDK", "href": "python-sdk.md", "hidden": True}
        )
    with open(args.path, "w") as f:
        content = yaml.dump(
            parsed, default_flow_style=False, sort_keys=False, Dumper=IndentListDumper
        )
        f.write(content)
