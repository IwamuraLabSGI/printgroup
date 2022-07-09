

set -ex



test -f ${PREFIX}/lib/libnettle${SHLIB_EXT}
test -f ${PREFIX}/lib/libhogweed${SHLIB_EXT}
test ! -f ${PREFIX}/lib/libnettle.a
test ! -f ${PREFIX}/lib/libhogweed.a
exit 0
