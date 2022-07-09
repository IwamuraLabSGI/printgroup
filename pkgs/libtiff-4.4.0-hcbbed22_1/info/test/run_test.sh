

set -ex



test -f ${PREFIX}/lib/libtiff.a
test -f ${PREFIX}/lib/libtiffxx.a
test -f ${PREFIX}/lib/libtiff.dylib
test -f ${PREFIX}/lib/libtiffxx.dylib
exit 0
