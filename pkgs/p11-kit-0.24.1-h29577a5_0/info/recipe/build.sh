#!/bin/bash
set -x

if [[ $CONDA_BUILD_CROSS_COMPILATION == "1" ]]; then
    # Get an updated config.sub and config.guess
    cp $BUILD_PREFIX/share/gnuconfig/config.* .
    # We need to regenerate the configs for osx-arm64, but we can't use autogen.sh because
    # 1. it's not included in the release tarball
    # 2. it's a sh script, which would mess up the shell env upon execution
    # see https://github.com/p11-glue/p11-kit/blob/7ea59012c2c81473132211e29ea8ebcc1ce31d09/autogen.sh#L19
    autoreconf --force --install --verbose
fi

./configure --prefix=$PREFIX \
            --with-trust-paths=$PREFIX/ssl/cert.pem
make
if [[ $CONDA_BUILD_CROSS_COMPILATION != "1" ]]; then
    make check
fi
make install
