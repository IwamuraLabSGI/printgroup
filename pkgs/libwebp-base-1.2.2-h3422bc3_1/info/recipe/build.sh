#!/bin/bash
# Get an updated config.sub and config.guess
cp $BUILD_PREFIX/share/libtool/build-aux/config.* .

# The libwebp build script doesn't pick all the other libraries up on its own
# (even though it should by using PREFIX), so pass all the necessary parameters
# for finding other imaging libraries to the configure script.
./configure --prefix=${PREFIX} --disable-gl --disable-dependency-tracking \
	--enable-libwebpmux --disable-libwebpdemux --enable-libwebpdecoder
make -j${CPU_COUNT}
if [[ "${CONDA_BUILD_CROSS_COMPILATION}" != "1" ]]; then
make check
fi
make install
