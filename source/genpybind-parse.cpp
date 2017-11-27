#include "clang/Frontend/ASTUnit.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Frontend/FrontendActions.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/PrettyStackTrace.h"
#include "llvm/Support/Signals.h"
#include "llvm/Support/TargetSelect.h"

#include "GenpybindExpandASTConsumer.h"

static llvm::cl::extrahelp
    CommonHelp(clang::tooling::CommonOptionsParser::HelpMessage);

static llvm::cl::OptionCategory
    GenpybindParseCategory("genpybind-parse options");
static llvm::cl::opt<std::string>
    OutputFile("output-file", llvm::cl::desc("where to save the AST dump"),
               llvm::cl::cat(GenpybindParseCategory));

namespace {

class ASTFrontendAction : public clang::ASTFrontendAction {
public:
  // We can not use TU_Prefix, since that leads to `Sema->TUScope == nullptr`,
  // which leads to segfaults and undefined behavior when synthesizing code.
  // clang::TranslationUnitKind getTranslationUnitKind() override {
  //   return clang::TU_Prefix;
  // }

  // We need to enable incremental preprocessing, s.t. TUScope is not
  // reset during the first call to `Sema::ActOnEndOfTranslationUnit`
  // before we get the chance to modify it in `HandleTranslationUnit`.
  bool BeginSourceFileAction(clang::CompilerInstance &CI) override {
    CI.getPreprocessor().enableIncrementalProcessing();
    return true;
  }

  std::unique_ptr<clang::ASTConsumer>
  CreateASTConsumer(clang::CompilerInstance &, StringRef) override {
    return llvm::make_unique<GenpybindExpandASTConsumer>();
  }
}; // ASTFrontendAction

class ASTBuilderAction : public clang::tooling::ToolAction {
  std::unique_ptr<clang::ASTUnit> &AST;

public:
  ASTBuilderAction(std::unique_ptr<clang::ASTUnit> &AST) : AST(AST) {}

  bool
  runInvocation(std::shared_ptr<clang::CompilerInvocation> Invocation,
                clang::FileManager *Files,
                std::shared_ptr<clang::PCHContainerOperations> PCHContainerOps,
                clang::DiagnosticConsumer *DiagConsumer) override {
    ASTFrontendAction Action;
    // FIXME: does not support FileManager argument
    AST.reset(clang::ASTUnit::LoadFromCompilerInvocationAction(
        Invocation, std::move(PCHContainerOps),
        clang::CompilerInstance::createDiagnostics(
            &Invocation->getDiagnosticOpts(), DiagConsumer,
            /*ShouldOwnClient=*/false),
        &Action));

    if (!AST)
      return false;

    return true;
  }
};

} // namespace

int main(int Argc, const char **Argv) {
  llvm::EnablePrettyStackTrace();
  llvm::sys::PrintStackTraceOnErrorSignal(Argv[0]);

  clang::tooling::CommonOptionsParser OptionsParser(
      Argc, Argv, GenpybindParseCategory,
      /*OccurrencesFlag=*/llvm::cl::Required);
  const std::vector<std::string> &SourcePathList =
      OptionsParser.getSourcePathList();
  assert(SourcePathList.size() == 1);
  clang::tooling::ClangTool Tool(OptionsParser.getCompilations(),
                                 SourcePathList);

  std::unique_ptr<clang::ASTUnit> AST;
  ASTBuilderAction Action(AST);

  int Status = Tool.run(&Action);

  if (!AST) {
    llvm::errs() << "No AST produced.\n";
    return 1;
  }

  if (OutputFile.empty())
    return Status;

  AST->Save(OutputFile);

  return Status;
}
