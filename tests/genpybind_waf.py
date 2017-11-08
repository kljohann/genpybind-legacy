import os
import pipes

from waflib import Logs, Task, Context, Errors
from waflib.Tools.c_preproc import scan as scan_impl
# ^-- Note: waflib.extras.gccdeps.scan does not work for us,
# due to its current implementation:
# The -MD flag is injected into the {C,CXX}FLAGS environment variable and
# dependencies are read out in a separate step after compiling by reading
# the .d file saved alongside the object file.
# As the genpybind task refers to a header file that is never compiled itself,
# gccdeps will not be able to extract the list of dependencies.

from waflib.TaskGen import feature, before_method

def configure(cfg):
    cfg.load('compiler_cxx')
    cfg.load('python')
    cfg.check_python_version(minver=(2, 7))
    cfg.find_program('genpybind', var='GENPYBIND')
    cfg.find_program('genpybind-parse', var='GENPYBIND_PARSE')
    if not cfg.env.LLVMCONFIG:
        cfg.find_program('llvm-config', var='LLVMCONFIG')

    # If genpybind-parse does not live in same prefix as llvm-config
    # we have to provide the -resource-dir argument.

    genpybind_parse_path = os.path.dirname(cfg.env.GENPYBIND_PARSE[0])
    llvm_config_path = os.path.dirname(cfg.env.LLVMCONFIG[0])
    if genpybind_parse_path != llvm_config_path:
        version, libdir = cfg.cmd_and_log(
            cfg.env.LLVMCONFIG + ["--version", "--libdir"],
            output=Context.STDOUT, quiet=Context.STDOUT,
        ).strip().split("\n")
        resource_dir = os.path.join(libdir, "clang", version)
        if not os.path.exists(resource_dir):
            cfg.fatal("could not find resource dir ({} does not exist)".format(
                resource_dir))
        cfg.env.CLANG_RESOURCE_DIR = resource_dir

def flatten(it):
    result = []
    stack = [list(it)]
    while stack:
        if not stack[-1]:
            stack.pop()
            continue

        elem = stack[-1].pop()
        if isinstance(elem, list):
            stack.append(elem[:])
        else:
            result.append(elem)
    result.reverse()
    return result

class genpybind(Task.Task):
    """
    Runs genpybind on headers provided as input to this task.
    Generated code will be written to the first (and only) output node.
    """
    quiet = True
    color = 'PINK'
    scan = scan_impl

    def keyword(self):
        return 'Analyzing'

    def _include_paths(self):
        return self.generator.to_incnodes(self.includes + self.env.INCLUDES)

    def _inputs_as_relative_includes(self):
        include_paths = self._include_paths()
        relative_includes = []
        for n in self.inputs:
            for inc in include_paths:
                if n.is_child_of(inc):
                    relative_includes.append(n.path_from(inc))
                    break
            else:
                self.generator.bld.fatal("could not resolve {}".format(n))
        return relative_includes

    def run(self):
        if not self.inputs:
            return

        bld = self.generator.bld
        relative_includes = self._inputs_as_relative_includes()
        is_cxx = "cxx" in self.features

        tool_path = bld.env.GENPYBIND
        genpybind_parse = bld.env.GENPYBIND_PARSE
        resource_dir = bld.env.CLANG_RESOURCE_DIR

        if not tool_path:
            bld.fatal("genpybind executable not found")

        args = flatten([
            tool_path,

            # options for genpybind
            "--genpybind-module", self.module,
            ["--genpybind-tag"] + self.genpybind_tags if self.genpybind_tags else [],
            ["--genpybind-include"] + relative_includes if relative_includes else [],
            ["--genpybind-parse"] + genpybind_parse if genpybind_parse else [],

            "--",
            # headers to be processed by genpybind
            [n.abspath() for n in self.inputs],

            "--",
            # options for clang/genpybind-parse
            "-D__GENPYBIND__",
            "-xc++" if is_cxx else "-xc",
            [flag.replace("-std=gnu", "-std=c")
             for flag in self.env["CXXFLAGS" if is_cxx else "CFLAGS"]],
            ["-I{}".format(n.abspath()) for n in self._include_paths()],
            ["-D{}".format(p) for p in self.env.DEFINES],

            # point to clang resource dir, if specified
            ["-resource-dir={}".format(resource_dir)] if resource_dir else [],
        ])

        # For debugging / log output
        pasteable_command = " ".join(pipes.quote(arg) for arg in args)

        # genpybind emits generated code to stdout
        try:
            stdout, stderr = bld.cmd_and_log(
                args, cwd=bld.variant_dir,
                output=Context.BOTH, quiet=Context.BOTH)
            if stderr.strip():
                Logs.debug("non-fatal warnings during genbybind run:\n{}".format(stderr))
        except Errors.WafError as e:
            bld.fatal(
                "genpybind returned {code} during the following call:"
                "\n{command}\n\n{stdout}\n\n{stderr}".format(
                    code=e.returncode,
                    command=pasteable_command,
                    stdout=e.stdout,
                    stderr=e.stderr,
                ))

        # write generated code to file in build directory
        # (will be compiled during process_source stage)
        (output_node,) = self.outputs
        output_node.write("// {}\n{}\n".format(
            pasteable_command.replace("\n", "\n// "), stdout))

@feature('genpybind')
@before_method('process_source')
def generate_genpybind_source(self):
    """
    Run genpybind on the headers provided in `source` and compile/link the
    generated code instead.  This works by generating the code on the fly and
    swapping the source node before `process_source` is run.
    """
    # name of module defaults to name of target
    module = getattr(self, 'module', self.target)

    # create temporary source file in build directory to hold generated code
    out = 'genpybind-%s.%d.cpp' % (module, self.idx)
    out = self.path.get_bld().find_or_declare(out)

    task = self.create_task("genpybind", self.to_nodes(self.source), out)
    # used to detect whether CFLAGS or CXXFLAGS should be passed to genpybind
    task.features = self.features
    task.module = module
    # can be used to select definitions to include in the current module
    # (when header files are shared by more than one module)
    task.genpybind_tags = self.to_list(getattr(self, 'genpybind_tags', []))
    # additional include directories
    task.includes = self.to_list(getattr(self, 'includes', []))

    # Tell waf to compile/link the generated code instead of the headers
    # originally passed-in via the `source` parameter. (see `process_source`)
    self.source = [out]
