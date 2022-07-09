

set -ex



touch checksum.txt
$PREFIX/bin/openssl sha256 checksum.txt
exit 0
