import os
import pipes
import subprocess
import sys

from waflib import Logs, Task, Context
from waflib.Tools.c_preproc import scan as scan_impl
# ^-- Note: waflib.extras.gccdeps.scan does not work for us,
# due to its current implementation:
# The -MD flag is injected into the {C,CXX}FLAGS environment variable and
# dependencies are read out in a separate step after compiling by reading
# the .d file saved alongside the object file.
# As the genpybind task refers to a header file that is never compiled itself,
# gccdeps will not be able to extract the list of dependencies.

from waflib.TaskGen import feature, before_method


def join_args(args):
    return " ".join(pipes.quote(arg) for arg in args)


def configure(cfg):
    cfg.load("compiler_cxx")
    cfg.load("python")
    cfg.check_python_version(minver=(2, 7))
    if not cfg.env.LLVM_CONFIG:
        cfg.find_program("llvm-config", var="LLVM_CONFIG")


@feature("genpybind")
@before_method("process_source")
def generate_genpybind_source(self):
    """
    Run genpybind on the headers provided in `source` and compile/link the
    generated code instead.  This works by generating the code on the fly and
    swapping the source node before `process_source` is run.
    """
    # name of module defaults to name of target
    module = getattr(self, "module", self.target)

    # create temporary source file in build directory to hold generated code
    out = "genpybind-%s.%d.cpp" % (module, self.idx)
    out = self.path.get_bld().find_or_declare(out)

    task = self.create_task("genpybind", self.to_nodes(self.source), out)
    # used to detect whether CFLAGS or CXXFLAGS should be passed to genpybind
    task.features = self.features
    task.module = module
    # can be used to select definitions to include in the current module
    # (when header files are shared by more than one module)
    task.genpybind_tags = self.to_list(getattr(self, "genpybind_tags", []))
    # additional include directories
    task.includes = self.to_list(getattr(self, "includes", []))
    node = self.bld.get_tgen_by_name("genpybind-parse").link_task.outputs[0]
    task.dep_nodes.append(node)
    task.genpybind_parse = node.abspath()

    # Tell waf to compile/link the generated code instead of the headers
    # originally passed-in via the `source` parameter. (see `process_source`)
    self.source = [out]


class genpybind(Task.Task): # pylint: disable=invalid-name
    """
    Runs genpybind on headers provided as input to this task.
    Generated code will be written to the first (and only) output node.
    """
    quiet = True
    color = "PINK"
    scan = scan_impl

    @staticmethod
    def keyword():
        return "Analyzing"

    def run(self):
        if not self.inputs:
            return

        args = self.find_genpybind() + self._arguments(
            genpybind_parse=self.genpybind_parse,
            resource_dir=self.find_resource_dir())

        output = self.run_genpybind(args)

        # For debugging / log output
        pasteable_command = join_args(args)

        # write generated code to file in build directory
        # (will be compiled during process_source stage)
        (output_node,) = self.outputs
        output_node.write("// {}\n{}\n".format(
            pasteable_command.replace("\n", "\n// "), output))

    def find_genpybind(self):
        return self.env.PYTHON + ["-m", "genpybind"]

    def find_resource_dir(self):
        """
        As genpybind-parse does not live in the same prefix as llvm-config
        we may have to provide the -resource-dir argument.
        """
        bld = self.generator.bld
        version, libdir = bld.cmd_and_log(
            bld.env.LLVM_CONFIG + ["--version", "--libdir"],
            output=Context.STDOUT, quiet=Context.STDOUT,
        ).strip().split("\n")
        resource_dir = os.path.join(libdir, "clang", version.replace("svn", ""))
        if not os.path.exists(resource_dir):
            bld.fatal("could not find resource dir ({} does not exist)".format(
                resource_dir))
        return resource_dir

    def run_genpybind(self, args):
        bld = self.generator.bld

        tgen = bld.get_tgen_by_name("genpybind")
        assert "py" in tgen.features
        pypath = getattr(tgen, "install_from", tgen.path).abspath()

        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join(
            filter(None, [pypath, env.get("PYTHONPATH")]))

        kwargs = dict(env=env, cwd=bld.variant_dir)
        bld.log_command(args, kwargs)
        proc = subprocess.Popen(
            args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
        stdout, stderr = proc.communicate()

        if not isinstance(stdout, str):
            stdout = stdout.decode(sys.stdout.encoding, errors="replace")
        if not isinstance(stderr, str):
            stderr = stderr.decode(sys.stderr.encoding, errors="replace")

        if proc.returncode != 0:
            bld.fatal(
                "genpybind returned {code} during the following call:"
                "\n{command}\n\n{stdout}\n\n{stderr}".format(
                    code=proc.returncode,
                    command=join_args(args),
                    stdout=stdout,
                    stderr=stderr,
                ))

        if stderr.strip():
            Logs.debug("non-fatal warnings during genpybind run:\n{}".format(stderr))

        return stdout

    def _include_paths(self):
        return self.generator.to_incnodes(self.includes + self.env.INCLUDES)

    def _inputs_as_relative_includes(self):
        include_paths = self._include_paths()
        relative_includes = []
        for node in self.inputs:
            for inc in include_paths:
                if node.is_child_of(inc):
                    relative_includes.append(node.path_from(inc))
                    break
            else:
                self.generator.bld.fatal("could not resolve {}".format(node))
        return relative_includes

    def _arguments(self, genpybind_parse=None, resource_dir=None):
        args = []
        relative_includes = self._inputs_as_relative_includes()
        is_cxx = "cxx" in self.features

        # options for genpybind
        args.extend(["--genpybind-module", self.module])
        if self.genpybind_tags:
            args.extend(["--genpybind-tag"] + self.genpybind_tags)
        if relative_includes:
            args.extend(["--genpybind-include"] + relative_includes)
        if genpybind_parse:
            args.extend(["--genpybind-parse", genpybind_parse])

        args.append("--")

        # headers to be processed by genpybind
        args.extend(node.abspath() for node in self.inputs)

        args.append("--")

        # options for clang/genpybind-parse
        args.append("-D__GENPYBIND__")
        args.append("-xc++" if is_cxx else "-xc")
        args.extend(
            flag.replace("-std=gnu", "-std=c")
            .replace("-std=c++11", "-std=c++17") # FIXME: move to genpybind-parse tool
            for flag in self.env["CXXFLAGS" if is_cxx else "CFLAGS"])
        args.extend("-I{}".format(n.abspath()) for n in self._include_paths())
        args.extend("-D{}".format(p) for p in self.env.DEFINES)

        # point to clang resource dir, if specified
        if resource_dir:
            args.append("-resource-dir={}".format(resource_dir))

        return args
