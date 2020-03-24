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


def artifact_path(target_name: str) -> Path:
    snapshots: Path = Path(__file__).resolve().parent / "expected"
    path = (snapshots / target_name).with_suffix(".txt")
    version_specific_path = path.with_suffix(".py{}.{}.txt".format(*sys.version_info))
    if version_specific_path.is_file():
        return version_specific_path
    return path


def load_expected_description(target_name: str) -> Optional[str]:
    path = artifact_path(target_name)
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("header", type=Path)
    # TODO: --interactive with os.isatty?
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    path = artifact_path(args.header.stem)

    expected = load_expected_description(args.header.stem) or ""
    try:
        actual = describe(args.header.stem)
    except ModuleNotFoundError as error:
        actual = str(error)
    diff = list(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected/" + path.name,
            tofile="actual/" + path.name,
        )
    )
    sys.stderr.writelines(diff)

    if args.update:
        path.write_text(actual, encoding="utf-8")
        print("Updated snapshot.")
    elif diff:
        print("Generated output does not match snapshot.")
        sys.exit(1)


if __name__ == "__main__":
    main()
