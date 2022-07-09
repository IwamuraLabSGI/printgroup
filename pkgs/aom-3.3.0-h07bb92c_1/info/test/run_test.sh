

set -ex



test -f ${PREFIX}/include/aom/aom.h
test -f ${PREFIX}/lib/libaom${SHLIB_EXT}
test ! -f ${PREFIX}/lib/libaom.a
test -f ${PREFIX}/lib/pkgconfig/aom.pc
exit 0
