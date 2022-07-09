

set -ex



test -f ${PREFIX}/include/x264.h
test -f ${PREFIX}/lib/libx264.a
test -f ${PREFIX}/lib/libx264.dylib
test -f ${PREFIX}/lib/libx264.161.dylib
x264 --help
exit 0
