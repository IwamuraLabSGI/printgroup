#!/bin/bash
# Get an updated config.sub and config.guess
cp $BUILD_PREFIX/share/libtool/build-aux/config.* .

OPTS=""
if [[ $(uname) == Darwin ]]; then
  OPTS="--disable-openmp"
fi
if [ "${target_platform}" == linux-ppc64le ]; then
  OPTS="--disable-vmx "
fi

export CFLAGS="-fPIC ${CFLAGS}"

./configure --prefix=$PREFIX \
            --host=${HOST} \
            $OPTS

make -j${CPU_COUNT} ${VERBOSE_AT}
if [[ "${CONDA_BUILD_CROSS_COMPILATION}" != "1" ]]; then
make check || { cat test/test-suite.log; exit 1; }
fi
make install

# We can remove this when we start using the new conda-build.
find $PREFIX -name '*.la' -delete
