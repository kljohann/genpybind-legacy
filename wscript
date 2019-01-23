#!/usr/bin/env python

top = "."
out = "build"

def options(opt):
    opt.load("python")
    opt.load("compiler_cxx")
    opt.add_option(
        "--disable-tests", action="store_true", default=False,
        dest="tests_disabled", help="Disable building and execution of tests")
    opt.add_option(
        "--clang-use-shared", action="store_true", default=False,
        dest="clang_use_shared",
        help="Indicate that clang was built using BUILD_SHARED_LIBS=ON")
    opt.recurse("tests")

def configure(cfg):
    cfg.load("python")
    cfg.load("compiler_cxx")
    cfg.check_python_version((2, 7))

    if not cfg.env.LLVM_CONFIG:
        cfg.find_program("llvm-config", var="LLVM_CONFIG")
    cfg.check_cfg(
        path=cfg.env.LLVM_CONFIG,
        atleast_version="5.0.0",
        args="--cxxflags --ldflags --libs --system-libs",
        uselib_store="LLVM",
        package="option support native",
        msg="Checking for LLVM libraries",
    )

    cfg.check(
        features="cxx cxxprogram",
        use="LLVM",
        uselib_store="CLANG",
        header_name=["clang/Basic/LLVM.h"], # check some arbitrary header
    )

    clang_libtype = 'lib' if cfg.options.clang_use_shared else 'stlib'
    cfg.check(
        features="cxx cxxprogram",
        use="LLVM",
        uselib_store="CLANG",
        **{clang_libtype: [
            "clangFrontend",
            "clangDriver",
            "clangSema",
            "clangAnalysis",
            "clangAST",
            "clangParse",
            "clangBasic",
            "clangEdit",
            "clangLex",
            "clangSerialization",
            "clangTooling",
            "clangSema",
            "clangToolingCore",
        ]})
    var = "{}PATH_CLANG".format(clang_libtype.upper())
    if not cfg.env[var]:
        cfg.env[var] = cfg.env.LIBPATH_LLVM

    cfg.env.TESTS_DISABLED = cfg.options.tests_disabled
    if not cfg.env.TESTS_DISABLED:
        cfg.recurse("tests")


def build(bld):
    bld.install_files(
        dest="${PREFIX}/bin",
        files=bld.path.ant_glob("bin/*"),
        chmod=0o755,
    )

    bld.install_files(
        dest="${PREFIX}/include",
        files='genpybind.h',
    )

    bld(
        target="genpybind",
        features="py",
        source=bld.path.ant_glob("genpybind/**/*.py"),
        install_from=".",
    )

    bld(
        target="genpybind-parse",
        features="cxx cxxprogram",
        source=[
            "source/genpybind-parse.cpp",
            "source/GenpybindExpandASTConsumer.cpp",
        ],
        use="LLVM CLANG",
    )

    if not bld.env.TESTS_DISABLED:
        bld.recurse("tests")
