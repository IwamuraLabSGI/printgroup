

set -ex



test -f ${PREFIX}/lib/libx265${SHLIB_EXT}
test ! -f ${PREFIX}/lib/libx265.a
test -f ${PREFIX}/lib/pkgconfig/x265.pc
test -f ${PREFIX}/include/x265.h
exit 0
