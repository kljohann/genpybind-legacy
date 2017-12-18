#pragma once
#include <queue>

#include <clang/Sema/SemaConsumer.h>

namespace clang {
class DeclContext;
} // namespace clang

class GenpybindExpandASTConsumer : public clang::SemaConsumer {
  clang::Sema *Sema = nullptr;
  std::queue<clang::CXXRecordDecl *> RecordDecls;

public:
  void InitializeSema(clang::Sema &Sema_) override;
  void ForgetSema() override;

  void HandleTagDeclDefinition(clang::TagDecl *D) override;
  void HandleTranslationUnit(clang::ASTContext &Ctx) override;

private:
  void AddImplicitMethods(clang::CXXRecordDecl *RD);
  void InstantiateTypedefTargets(clang::DeclContext *DC);
  bool ShouldMethodBeReferenced(clang::CXXMethodDecl const *M) const;
}; // GenpybindExpandASTConsumer
