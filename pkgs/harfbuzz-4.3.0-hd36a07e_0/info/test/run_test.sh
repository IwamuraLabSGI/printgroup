

set -ex



test -f $PREFIX/lib/libharfbuzz-gobject${SHLIB_EXT}
test -f $PREFIX/lib/libharfbuzz-icu${SHLIB_EXT}
test -f $PREFIX/lib/libharfbuzz${SHLIB_EXT}
test -f $PREFIX/include/harfbuzz/hb-ft.h
test -f $PREFIX/lib/girepository-1.0/HarfBuzz-0.0.typelib
exit 0
