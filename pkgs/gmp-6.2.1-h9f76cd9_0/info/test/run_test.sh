eval "${CC} -I ${PREFIX}/include -L ${PREFIX}/lib test.c -lgmp -Wl,-rpath,${PREFIX}/lib -o test.out"
./test.out


set -ex



test -f ${PREFIX}/lib/libgmp.a
test -f ${PREFIX}/lib/libgmp.dylib
test -f ${PREFIX}/lib/libgmpxx.a
test -f ${PREFIX}/lib/libgmpxx.dylib
exit 0
