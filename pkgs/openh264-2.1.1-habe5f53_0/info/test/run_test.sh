

set -ex



h264enc -h
test -f $PREFIX/bin/h264dec
test -f $PREFIX/lib/libopenh264.dylib
exit 0
