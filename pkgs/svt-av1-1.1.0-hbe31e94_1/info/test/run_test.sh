

set -ex



test -f $PREFIX/include/svt-av1/EbSvtAv1.h
test -f $PREFIX/lib/libSvtAv1Dec${SHLIB_EXT}
test -f $PREFIX/lib/libSvtAv1Enc${SHLIB_EXT}
exit 0
