#!/bin/bash

set -ex

mkdir build-stage
cd build-stage


cmake ${CMAKE_ARGS} -DCMAKE_BUILD_TYPE="Release"   \
      -DCMAKE_INSTALL_PREFIX=${PREFIX}             \
      -DCMAKE_INSTALL_LIBDIR:PATH=${PREFIX}/lib    \
      -DBUILD_SHARED_LIBS=ON                       \
      -DENABLE_DOCS=OFF                            \
      -DENABLE_EXAMPLES=ON                         \
      -DENABLE_TESTS=OFF                           \
      ..

# Parallel build fails spuriously, so only build in serial
make

# beware, tests are expensive (data downloads & many of them, some fairly slow)
# to enable: set cmake above, uncomment python in meta.yaml, uncomment below
# make -j${CPU_COUNT} runtests

make install

# Even if you build shared libraries, the static ones still
# get installed
# Remove static libraries that are installed
# https://github.com/conda-forge/aom-feedstock/issues/7
rm ${PREFIX}/lib/*.a
