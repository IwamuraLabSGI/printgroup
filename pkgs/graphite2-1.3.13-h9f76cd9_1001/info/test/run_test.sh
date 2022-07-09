

set -ex



conda inspect linkages -p $PREFIX $PKG_NAME
conda inspect objects -p $PREFIX $PKG_NAME
exit 0
