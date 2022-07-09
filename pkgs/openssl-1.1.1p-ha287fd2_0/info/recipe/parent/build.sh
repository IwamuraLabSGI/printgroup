#!/bin/bash

PERL=${PREFIX}/bin/perl
declare -a _CONFIG_OPTS
_CONFIG_OPTS+=(--prefix=${PREFIX})
_CONFIG_OPTS+=(--libdir=lib)
_CONFIG_OPTS+=(shared)
_CONFIG_OPTS+=(threads)
_CONFIG_OPTS+=(enable-ssl2)
_CONFIG_OPTS+=(no-zlib)

# We are cross-compiling or using a specific compiler.
# do not allow config to make any guesses based on uname.
_CONFIGURATOR="perl ./Configure"
case "$target_platform" in
  linux-64)
    _CONFIG_OPTS+=(linux-x86_64)
    CFLAGS="${CFLAGS} -Wa,--noexecstack"
    ;;
  linux-aarch64)
    _CONFIG_OPTS+=(linux-aarch64)
    CFLAGS="${CFLAGS} -Wa,--noexecstack"
    ;;
  linux-ppc64le)
    _CONFIG_OPTS+=(linux-ppc64le)
    CFLAGS="${CFLAGS} -Wa,--noexecstack"
    ;;
  osx-64)
    _CONFIG_OPTS+=(darwin64-x86_64-cc)
    ;;
  osx-arm64)
    _CONFIG_OPTS+=(darwin64-arm64-cc)
    ;;
esac

CC=${CC}" ${CPPFLAGS} ${CFLAGS}" \
  ${_CONFIGURATOR} ${_CONFIG_OPTS[@]} ${LDFLAGS}

make -j${CPU_COUNT}

if [[ "${CONDA_BUILD_CROSS_COMPILATION}" != "1" ]]; then
  make test
fi
