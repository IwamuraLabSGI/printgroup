

set -ex



test -f $PREFIX/lib/libwebp.a
test -f $PREFIX/lib/libwebp.dylib
test -f $PREFIX/lib/libwebpmux.dylib
test -f $PREFIX/include/webp/decode.h
test -f $PREFIX/include/webp/encode.h
test -f $PREFIX/include/webp/types.h
exit 0
