from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import shutil
import subprocess
import sys
import tempfile

from clang.cindex import TranslationUnit

from .decls import gather_declarations
from .expose import expose_as

def main():
    # type: () -> None
    parser = argparse.ArgumentParser()

    parser.add_argument("--genpybind-module", dest="module", required=True)
    parser.add_argument("--genpybind-parse", dest="executable", default="genpybind-parse")
    parser.add_argument("--genpybind-docstring", dest="docstring")
    parser.add_argument("--genpybind-include", nargs="+", dest="includes")
    parser.add_argument("--genpybind-isystem", nargs="+", dest="isystem")
    parser.add_argument("--genpybind-tag", nargs="+", dest="tags")
    parser.add_argument("--genpybind-from-ast", dest="from_ast")
    parser.add_argument('rest', nargs=argparse.REMAINDER)

    # args, rest_args = parser.parse_known_args()
    args = parser.parse_args()

    if args.from_ast:
        if args.rest:
            parser.error(
                "unexpected arguments with --genpybind-from-ast: {}".format(args.rest))
        translation_unit = TranslationUnit.from_ast_file(args.from_ast)
    else:
        name = tempfile.mkdtemp(prefix="genpybind")
        ast_file = os.path.join(name, "genpybind.ast")
        try:
            rest = args.rest[:]
            if rest[0] == "--":
                del rest[0]
            status = subprocess.call(
                [args.executable, "-output-file", ast_file] + rest, stdout=sys.stderr)
            if status != 0:
                parser.error("genpybind-parse returned status {} when called with\n{}".format(
                    status, rest))
            translation_unit = TranslationUnit.from_ast_file(ast_file)
        finally:
            shutil.rmtree(name, ignore_errors=True)

    if translation_unit.diagnostics:
        for diag in translation_unit.diagnostics:
            print("//", diag.format())
            for diag_ in diag.children:
                print("//", "  ", diag_.format())

    toplevel_declarations = gather_declarations(translation_unit.cursor)

    print(expose_as(
        toplevel_declarations,
        module=args.module,
        doc=args.docstring,
        isystem=args.isystem,
        includes=args.includes,
        tags=args.tags,
    ))
