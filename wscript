#!/usr/bin/env python

top = "."
out = "build"

def options(opt):
    opt.load("python")
    opt.load("compiler_cxx")
    opt.add_option(
        "--disable-tests", action="store_true", default=False,
        dest="tests_disabled", help="Disable building and execution of tests")
    opt.recurse("tests")

def configure(cfg):
    cfg.load("python")
    cfg.load("compiler_cxx")
    cfg.check_python_version((2, 7))

    if not cfg.env.LLVMCONFIG:
        cfg.find_program("llvm-config", var="LLVMCONFIG")
    cfg.check_cfg(
        path=cfg.env.LLVMCONFIG,
        atleast_version="5.0.0",
        args="--cxxflags --libs --system-libs",
        uselib_store="LLVM",
        package="option support native",
        msg="Checking for LLVM libraries",
    )

    cfg.check(
        features="cxx cxxprogram",
        use="LLVM",
        uselib_store="CLANG",
        header_name=["clang/AST/AST.h"],
    )

    for lib in [
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
    ]:
        cfg.check(
            features="cxx cxxprogram",
            use="LLVM",
            uselib_store="CLANG",
            stlib=lib,
        )

    cfg.env.TESTS_DISABLED = cfg.options.tests_disabled
    if not cfg.env.TESTS_DISABLED:
        cfg.recurse("tests")

def build(bld):
    bld.install_files(
        dest="${PREFIX}/bin",
        files=bld.path.ant_glob("bin/*"),
        chmod=0o755,
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
        cxxflags=["-fno-exceptions", "-fno-rtti"],
    )

    if not bld.env.TESTS_DISABLED:
        bld.recurse("tests")
