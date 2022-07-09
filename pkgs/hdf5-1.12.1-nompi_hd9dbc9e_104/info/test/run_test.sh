

set -ex



command -v h5c++
command -v h5cc
command -v h5fc
command -v h5redeploy
command -v gif2h5
command -v h52gif
command -v h5copy
command -v h5debug
command -v h5diff
command -v h5dump
command -v h5import
command -v h5jam
command -v h5ls
command -v h5mkgrp
command -v h5repack
command -v h5repart
command -v h5stat
command -v h5unjam
test -f $PREFIX/lib/libhdf5${SHLIB_EXT}
test -f $PREFIX/lib/libhdf5_cpp${SHLIB_EXT}
test -f $PREFIX/lib/libhdf5_hl${SHLIB_EXT}
test -f $PREFIX/lib/libhdf5_hl_cpp${SHLIB_EXT}
h5dump --filedriver=ros3 "http://s3.amazonaws.com/hdfgroup/data/hdf5demo/tall.h5" | grep '^HDF5'
exit 0
