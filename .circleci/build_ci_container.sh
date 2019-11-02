#!/bin/bash
set -e

readonly cmake_args="\
-DLLVM_TARGETS_TO_BUILD=X86 -DLLVM_PARALLEL_LINK_JOBS=2 \
-DLLVM_ENABLE_PROJECTS=clang \
-DCMAKE_BUILD_TYPE=Release"

readonly source_dir="$(dirname "$(readlink -e "${BASH_SOURCE[0]}")")"
readonly build_dir="$(mktemp -d)"
trap 'rm -rf "${build_dir}"' EXIT

cp -r "${source_dir}/../llvm-patches" "${build_dir}"

docker build -t "kljohann/genpybind-ci:0.9.0" \
  --build-arg "clone_args=--depth=1 -b release/9.x" \
  --build-arg "cmake_args=${cmake_args}" \
  -f "${source_dir}/Dockerfile" \
  "${build_dir}"
