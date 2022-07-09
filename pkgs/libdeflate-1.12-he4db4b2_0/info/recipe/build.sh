#!/bin/bash
set -x

make

# The make script uses the $PREFIX env variable to install the application.
# The 'gzip' application (which is not gzip) will be renamed libdeflate-gzip.
make install

# Remove static libraries that are installed automatically
rm -f $PREFIX/lib/libdeflate.a
