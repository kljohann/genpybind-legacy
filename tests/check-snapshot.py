#!/usr/bin/env python3
import argparse
import difflib
import importlib
import pydoc
import re
import sys

from pathlib import Path
from typing import Any, Optional

RE_MEMORY_ADDRESS = re.compile(" at 0x[0-9a-f]{6,}", re.I)
RE_TRAILING_WHITESPACE = re.compile("[ \t]*$", re.M)


class StablePlainTextDoc(pydoc.TextDoc):
    def bold(self, text: str) -> str:
        return text

    def section(self, title: str, contents: str) -> str:
        if title in ["FILE"]:
            return ""
        return super().section(title, contents)

    def document(self, *args: Any, **kwargs: Any) -> str:
        text: str = super().document(*args, **kwargs)
        text = RE_MEMORY_ADDRESS.sub("", text)
        text = RE_TRAILING_WHITESPACE.sub("", text)
        return text


def describe(target_name: str) -> str:
    module_name = "py" + target_name
    module = importlib.import_module(module_name)
    return StablePlainTextDoc().document(module)


def load_expected_description(artifact_path: Path) -> Optional[str]:
    if not artifact_path.is_file():
        return None
    return artifact_path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("header", type=Path)
    parser.add_argument("artifact", type=Path)
    # TODO: --interactive with os.isatty?
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    artifact_path = args.artifact

    expected = load_expected_description(artifact_path) or ""
    try:
        actual = describe(args.header.stem)
    except ModuleNotFoundError as error:
        actual = str(error)
    diff = list(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected/" + artifact_path.name,
            tofile="actual/" + artifact_path.name,
        )
    )
    sys.stderr.writelines(diff)

    if diff:
        if args.update:
            artifact_path.write_text(actual, encoding="utf-8")
            print("snapshot updated")
        else:
            print("snapshot does not match")
            sys.exit(1)
    else:
        print("snapshot matches")


if __name__ == "__main__":
    main()
