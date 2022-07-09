#!/bin/bash
# Get an updated config.sub and config.guess
cp $BUILD_PREFIX/share/libtool/build-aux/config.* .

./configure --prefix="${PREFIX}"  \
            --host="${HOST}"      \
            --enable-utf          \
            --enable-unicode-properties
make -j${CPU_COUNT} ${VERBOSE_AT}
if [[ "${CONDA_BUILD_CROSS_COMPILATION}" != "1" ]]; then
make check  || { cat ./test-suite.log; exit 1; }
fi
make install

# Delete man pages.
rm -rf "${PREFIX}/share"

# We can remove this when we start using the new conda-build.
find $PREFIX -name '*.la' -delete
