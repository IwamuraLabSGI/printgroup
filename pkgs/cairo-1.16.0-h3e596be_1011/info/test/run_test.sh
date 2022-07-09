

set -ex



cairo-trace --help
test -f $PREFIX/lib/libcairo.a
test -f $PREFIX/lib/libcairo.dylib
test -f $PREFIX/lib/libcairo-gobject.a
test -f $PREFIX/lib/libcairo-gobject.dylib
test -f $PREFIX/lib/libcairo-script-interpreter.a
test -f $PREFIX/lib/libcairo-script-interpreter.dylib
test -f $PREFIX/lib/pkgconfig/cairo-quartz.pc
test -f $PREFIX/include/cairo/cairo.h
grep -q "CAIRO_HAS_FC_FONT 1" $PREFIX/include/cairo/cairo-features.h
exit 0
