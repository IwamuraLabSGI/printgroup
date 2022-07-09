#!/bin/bash

declare -a CMAKE_PLATFORM_FLAGS
if [[ ${HOST} =~ .*linux.* ]]; then
    CMAKE_PLATFORM_FLAGS+=(-DCMAKE_TOOLCHAIN_FILE="${RECIPE_DIR}/cross-linux.cmake")
fi

mkdir build_shared && cd $_
cmake ${CMAKE_ARGS} \
    -DCMAKE_PREFIX_PATH=$PREFIX \
    -DCMAKE_INSTALL_PREFIX=$PREFIX \
    -DJAS_ENABLE_AUTOMATIC_DEPENDENCIES=False \
    ${CMAKE_PLATFORM_FLAGS[@]} ..
make -j${CPU_COUNT}
make install
cd ..

mkdir build_static && cd $_
cmake ${CMAKE_ARGS} \
    -DJAS_ENABLE_SHARED=OFF \
    -DCMAKE_PREFIX_PATH=$PREFIX \
    -DCMAKE_INSTALL_PREFIX=$PREFIX \
    -DJAS_ENABLE_AUTOMATIC_DEPENDENCIES=False \
    ${CMAKE_PLATFORM_FLAGS[@]} ..
make -j${CPU_COUNT}
make install
cd ..
