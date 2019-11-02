# --- stage 1: build LLVM ------------------------------------------------------

FROM bitnami/minideb:latest as builder
RUN install_packages \
    build-essential cmake ninja-build \
    python3 git ca-certificates

ARG clone_args
RUN mkdir -p /tmp/clang-build && \
    git clone https://github.com/llvm/llvm-project \
      /tmp/clang-build/src ${clone_args}

ADD llvm-patches /tmp/patches
RUN find /tmp/patches -name '*.patch' -print0 | \
    sort -z | xargs -0 -L1 \
    patch -d /tmp/clang-build/src -p1 -i

ARG cmake_args
RUN mkdir -p /tmp/clang-install /tmp/clang-build/build && \
    cd /tmp/clang-build/build && \
    cmake -GNinja \
      -DCMAKE_INSTALL_PREFIX=/tmp/clang-install \
      -DCLANG_PYTHON_BINDINGS_VERSIONS=3 \
      ${cmake_args} \
      /tmp/clang-build/src/llvm && \
    ninja \
      install-clang \
      install-clang-headers \
      install-clang-libraries \
      install-clang-resource-headers \
      install-libclang \
      install-libclang-headers \
      install-libclang-python-bindings \
      install-llvm-config \
      install-llvm-headers \
      install-llvm-libraries && \
    cd /tmp && rm -rf /tmp/clang-build/build && \
    find /tmp/clang-install -name site-packages \
         -execdir mv '{}' dist-packages \; -prune

# --- stage 2: create minimal image with build results -------------------------

FROM bitnami/minideb:latest
RUN install_packages \
    build-essential \
    python3 python3-dev python3-pip \
    git ca-certificates
COPY --from=builder /tmp/clang-install/ /usr/
