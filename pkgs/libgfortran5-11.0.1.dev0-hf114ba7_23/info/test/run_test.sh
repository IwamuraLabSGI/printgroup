

set -ex



test -f "${PREFIX}/lib/libgfortran.dylib"
test -f "${PREFIX}/lib/libgfortran.5.dylib"
test -f "${PREFIX}/lib/libgomp.dylib"
test -f "${PREFIX}/lib/libgomp.1.dylib"
test -f "${PREFIX}/lib/libquadmath.dylib"
test -f "${PREFIX}/lib/libquadmath.0.dylib"
test -f "${PREFIX}/lib/libgcc_s.2.dylib"
exit 0
