

set -ex



export MACOSX_DEPLOYMENT_TARGET=11.0
export CONDA_BUILD_SYSROOT=/Applications/Xcode_12.4.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX11.0.sdk
OPENCV_FLAGS=`pkg-config --cflags opencv4`
$CXX -std=c++11 $RECIPE_DIR/test.cpp ${OPENCV_FLAGS} -o test
if [[ $(./test) != $PKG_VERSION ]]; then exit 1 ; fi
test -f $PREFIX/lib/libopencv_alphamat${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_aruco${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_bgsegm${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_calib3d${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_ccalib${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_core${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_datasets${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_dnn_objdetect${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_dnn_superres${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_dnn${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_dpm${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_face${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_features2d${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_flann${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_fuzzy${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_gapi${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_hfs${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_highgui${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_img_hash${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_imgcodecs${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_imgproc${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_intensity_transform${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_line_descriptor${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_mcc${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_ml${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_objdetect${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_optflow${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_phase_unwrapping${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_photo${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_plot${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_quality${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_rapid${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_reg${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_rgbd${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_saliency${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_shape${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_stereo${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_stitching${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_structured_light${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_superres${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_surface_matching${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_text${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_tracking${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_video${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_videoio${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_videostab${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_wechat_qrcode${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_xfeatures2d${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_ximgproc${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_xobjdetect${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_xphoto${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_bioinspired${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_hdf${SHLIB_EXT}
test -f $PREFIX/lib/libopencv_freetype${SHLIB_EXT}
mkdir -p cmake_build_test && pushd cmake_build_test
cmake -G "Ninja" ..
cmake --build . --config Release
popd
exit 0
