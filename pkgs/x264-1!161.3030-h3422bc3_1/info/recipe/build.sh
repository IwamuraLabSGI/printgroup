#!/bin/bash
# Get an updated config.sub and config.guess
cp $BUILD_PREFIX/share/gnuconfig/config.* .
set -xe
mkdir -vp ${PREFIX}/bin

# Set the assembler to `nasm`
if [[ ${target_platform} == "linux-64" || ${target_platform} == osx-64 ]]; then
    export AS="${BUILD_PREFIX}/bin/nasm"
fi

if [[ "${target_platform}" == *-aarch64 || "${target_platform}" == *-arm64 ]]; then
    unset AS
fi

chmod +x configure
./configure \
        --host=$HOST \
        --enable-pic \
        --enable-shared \
        --enable-static \
        --prefix=${PREFIX}
make -j${CPU_COUNT}
make install
