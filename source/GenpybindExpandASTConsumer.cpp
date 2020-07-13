#include "GenpybindExpandASTConsumer.h"

#include <clang/AST/DeclCXX.h>
#include <clang/AST/RecursiveASTVisitor.h>
#include <clang/Sema/Sema.h>
#include <clang/Sema/SemaDiagnostic.h>

namespace {

/// Force default argument instantiation, s.t. the corresponding `Expr` node is
/// present in the AST.  (This is normally done lazily when gathering arguments
/// at the call site.)
class InstantiateDefaultArgsVisitor
    : public clang::RecursiveASTVisitor<InstantiateDefaultArgsVisitor> {
  clang::Sema *Sema = nullptr;

public:
  InstantiateDefaultArgsVisitor(clang::Sema *Sema) : Sema(Sema) {}

  bool shouldWalkTypesOfTypeLocs() const { return false; }
  bool shouldVisitTemplateInstantiations() const { return true; }
  bool shouldVisitImplicitCode() const { return false; }

  bool TraverseStmt(clang::Stmt *) {
    // Do not visit statements and expressions.
    return true;
  }

  bool VisitParmVarDecl(clang::ParmVarDecl *Decl) {
    if (Decl->hasUnparsedDefaultArg() || Decl->hasUninstantiatedDefaultArg())
      if (auto Function =
              llvm::dyn_cast<clang::FunctionDecl>(Decl->getDeclContext()))
        Sema->CheckCXXDefaultArgExpr(clang::SourceLocation(), Function, Decl);
    return true;
  }
};

} // namespace

void GenpybindExpandASTConsumer::InitializeSema(clang::Sema &Sema_) {
  Sema = &Sema_;
}

void GenpybindExpandASTConsumer::ForgetSema() { Sema = nullptr; }

void GenpybindExpandASTConsumer::HandleTagDeclDefinition(clang::TagDecl *D) {
  if (auto *RD = clang::dyn_cast<clang::CXXRecordDecl>(D)) {
    if (!RD->isDependentContext())
      this->RecordDecls.push(RD);
  }
}

void GenpybindExpandASTConsumer::HandleTranslationUnit(clang::ASTContext &Ctx) {
  if (Sema == nullptr)
    return;
  assert(Sema->TUScope != nullptr);

  Sema->PerformPendingInstantiations();

  if (Sema->getDiagnostics().hasErrorOccurred())
    return;

  // All diagnostics from this point on will be due to changes made here
  Sema->getDiagnostics().setSuppressAllDiagnostics(true);

  // HandleTagDeclDefinition may still be called due to instantiations effected below.
  while (!RecordDecls.empty()) {
    clang::CXXRecordDecl *RD = RecordDecls.front();
    RecordDecls.pop();

    if (Sema->getSourceManager().isInSystemHeader(RD->getLocation()))
      continue;

    Sema->ForceDeclarationOfImplicitMembers(RD);

    AddImplicitMethods(RD);
    InstantiateTypedefTargets(RD);

    Sema->PerformPendingInstantiations();
  }

  Sema->ActOnEndOfTranslationUnit();

  InstantiateDefaultArgsVisitor Visitor(Sema);
  Visitor.TraverseDecl(Ctx.getTranslationUnitDecl());
}

void GenpybindExpandASTConsumer::AddImplicitMethods(clang::CXXRecordDecl *RD) {
  assert(Sema != nullptr && RD != nullptr);

  for (clang::CXXMethodDecl *Method : RD->methods()) {
    if (ShouldMethodBeReferenced(Method))
      Sema->MarkFunctionReferenced(clang::SourceLocation(), Method);
  }
}

void GenpybindExpandASTConsumer::InstantiateTypedefTargets(
    clang::DeclContext *DC) {
  assert(Sema != nullptr && DC != nullptr);

  for (clang::Decl *D : DC->decls()) {
    if (auto const *Typedef = clang::dyn_cast<clang::TypedefNameDecl>(D)) {
      // if (Typedef->isTransparentTag())
      //   continue;

      clang::QualType QT = Typedef->getUnderlyingType();

      if (QT->isDependentType())
        continue;

      // Attempt to perform class template instantiation.
      bool IsIncomplete = Sema->RequireCompleteType(
          Typedef->getLocation(), QT, clang::diag::err_incomplete_type);
      static_cast<void>(IsIncomplete);
    }
  }
}

bool GenpybindExpandASTConsumer::ShouldMethodBeReferenced(
    clang::CXXMethodDecl const *M) const {
  assert(Sema != nullptr && M != nullptr);

  if (M->isDeleted() || M->isInvalidDecl())
    return false;

  if (auto *C = clang::dyn_cast<clang::CXXConstructorDecl>(M)) {
    return (C->isDefaultConstructor() || C->isCopyOrMoveConstructor());
  }

  if (clang::dyn_cast<clang::CXXDestructorDecl>(M))
    return true;

  if (M->isCopyAssignmentOperator() || M->isMoveAssignmentOperator())
    return true;

  return false;
}
