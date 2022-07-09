#!/bin/bash

# Based on
# - https://bitbucket.org/multicoreware/x265_git/src/master/build/linux/multilib.sh
# - https://github.com/Homebrew/homebrew-core/blob/master/Formula/x265.rb

set -ex

mkdir 8bit 10bit 12bit

cd 8bit

if [[ $target_platform == linux-ppc64le || $target_platform == linux-aarch64 ]]; then
    # linux-ppc64le and linux-aarch64 can not build 10bit/12bit support
    EXTRA_LIBS=""
    LINKED_BITS="OFF"
else

    # --- Pixel depth 12
    cd ../12bit
    cmake ${CMAKE_ARGS} ../source        \
        -DHIGH_BIT_DEPTH=ON              \
        -DEXPORT_C_API=OFF               \
        -DENABLE_SHARED=OFF              \
        -DENABLE_CLI=OFF                 \
        -DMAIN12=ON                      \
        -DCMAKE_BUILD_TYPE="Release"     \
        -DCMAKE_INSTALL_PREFIX=${PREFIX}

    make -j${CPU_COUNT}

    # --- Pixel depth 10
    cd ../10bit
    cmake ${CMAKE_ARGS} ../source        \
        -DHIGH_BIT_DEPTH=ON              \
        -DEXPORT_C_API=OFF               \
        -DENABLE_SHARED=OFF              \
        -DENABLE_CLI=OFF                 \
        -DENABLE_HDR10_PLUS=ON           \
        -DCMAKE_BUILD_TYPE="Release"     \
        -DCMAKE_INSTALL_PREFIX=${PREFIX}

    make -j${CPU_COUNT}

    EXTRA_LIBS="-DEXTRA_LIB=x265_main10.a;x265_main12.a"
    cd ../8bit
    ln -sf ../10bit/libx265.a libx265_main10.a
    ln -sf ../12bit/libx265.a libx265_main12.a
    LINKED_BITS="ON"
fi

# --- Pixel depth 8, and put it all together
cd ../8bit

cmake ${CMAKE_ARGS} ../source                    \
    -DCMAKE_BUILD_TYPE="Release"                 \
    -DCMAKE_INSTALL_PREFIX=${PREFIX}             \
    -DENABLE_SHARED=TRUE                         \
    -DLINKED_10BIT=$LINKED_BITS                  \
    -DLINKED_12BIT=$LINKED_BITS                  \
    -DEXTRA_LINK_FLAGS='-L .'                    \
    $EXTRA_LIBS

make -j${CPU_COUNT}

make install

# 2022/03/06: hmaarrfk
# x265 likes to install the static library no matter what
# Remove any installed static libraries
rm ${PREFIX}/lib/*.a
