

set -ex



test -f ${PREFIX}/lib/libglib-2.0.0.dylib
test ! -f ${PREFIX}/lib/libgobject-2.0.la
test ! -f ${PREFIX}/lib/libglib-2.0${SHLIB_EXT}
test -f ${PREFIX}/lib/pkgconfig/glib-2.0.pc
test -f ${PREFIX}/etc/conda/activate.d/libglib_activate.sh
test -f ${PREFIX}/etc/conda/deactivate.d/libglib_deactivate.sh
exit 0
