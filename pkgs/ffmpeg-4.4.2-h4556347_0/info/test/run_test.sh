

set -ex



ffmpeg --help
ffmpeg -loglevel panic -protocols | grep "https"
ffmpeg -loglevel panic -codecs | grep "libmp3lame"
ffmpeg -loglevel panic -codecs | grep "DEVI.S zlib"
ffmpeg -loglevel panic -codecs | grep "DEV.LS h264"
ffmpeg -loglevel panic -codecs | grep "libx264"
ffmpeg -loglevel panic -codecs | grep "libx265"
ffmpeg -loglevel panic -codecs | grep "libopenh264"
ffmpeg -loglevel panic -codecs | grep "libaom"
ffmpeg -loglevel panic -codecs | grep "libsvtav1"
test -f $PREFIX/lib/libavdevice${SHLIB_EXT}
test -f $PREFIX/lib/libswresample${SHLIB_EXT}
test -f $PREFIX/lib/libpostproc${SHLIB_EXT}
test -f $PREFIX/lib/libavfilter${SHLIB_EXT}
test -f $PREFIX/lib/libavcodec${SHLIB_EXT}
test -f $PREFIX/lib/libavformat${SHLIB_EXT}
test -f $PREFIX/lib/libswscale${SHLIB_EXT}
test -f $PREFIX/lib/libavresample${SHLIB_EXT}
test -f $PREFIX/lib/libavutil${SHLIB_EXT}
exit 0
