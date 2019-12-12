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

    parser.add_argument("--genpybind-module", dest="module", required=True,
                        help="name of the extension module (cf. PYBIND11_MODULE)")
    parser.add_argument("--genpybind-parse", dest="executable", default="genpybind-parse",
                        help="name of the tool used to extend/amend the abstract syntax tree")
    parser.add_argument("--genpybind-docstring", dest="docstring",
                        help="docstring of the extension module (cf. PYBIND11_MODULE)")
    parser.add_argument("--genpybind-include", nargs="+", dest="includes",
                        help="includes to add to the generated bindings file (added in \"\"")
    parser.add_argument("--genpybind-isystem", nargs="+", dest="isystem",
                        help="includes to add to the generated bindings file (added in <>)")
    parser.add_argument("--genpybind-tag", nargs="+", dest="tags",
                        help="generate bindings for tagged parts; otherwise tagged parts will be omitted from binding generation")
    parser.add_argument("--genpybind-from-ast", dest="from_ast",
                        help="read from already generated abstract syntax tree instead of calling genpybind-parse")
    parser.add_argument('rest', nargs=argparse.REMAINDER,
                        help="arguments to genpybind-parse; also including compiler flags for the regular processing of the translation unit corresponding to the header file")

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
            shutil.rmtree(name)

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
