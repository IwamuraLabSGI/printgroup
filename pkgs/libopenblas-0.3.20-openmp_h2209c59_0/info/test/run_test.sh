

set -ex



test -f ${PREFIX}/lib/libopenblasp-r0.3.20.dylib
nm -g ${PREFIX}/lib/libopenblasp-r0.3.20.dylib | grep dsecnd
python -c "import ctypes; ctypes.cdll['${PREFIX}/lib/libopenblasp-r0.3.20.dylib']"
exit 0
