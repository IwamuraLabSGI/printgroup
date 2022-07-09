@ECHO ON
mkdir 12bit
if errorlevel 1 exit 1
cd 12bit
if errorlevel 1 exit 1

cmake %CMAKE_ARGS% ..\source         ^
    -DCMAKE_BUILD_TYPE=Release       ^
    -DHIGH_BIT_DEPTH=ON              ^
    -DEXPORT_C_API=OFF               ^
    -DENABLE_SHARED=OFF              ^
    -DENABLE_CLI=OFF                 ^
    -DMAIN12=ON                      ^
    -DCMAKE_INSTALL_PREFIX=%LIBRARY_PREFIX%
if errorlevel 1 exit 1

cmake --build . --config Release --parallel %CPU_COUNT%
if errorlevel 1 exit 1
cd ..

mkdir 10bit
if errorlevel 1 exit 1
cd 10bit
if errorlevel 1 exit 1

cmake %CMAKE_ARGS% ..\source         ^
    -DCMAKE_BUILD_TYPE=Release       ^
    -DHIGH_BIT_DEPTH=ON              ^
    -DEXPORT_C_API=OFF               ^
    -DENABLE_SHARED=OFF              ^
    -DENABLE_CLI=OFF                 ^
    -DENABLE_HDR10_PLUS=ON           ^
    -DCMAKE_INSTALL_PREFIX=%LIBRARY_PREFIX%
if errorlevel 1 exit 1
cmake --build . --config Release --parallel %CPU_COUNT%
if errorlevel 1 exit 1
cd ..

mkdir 8bit
if errorlevel 1 exit 1
cd 8bit
if errorlevel 1 exit 1

copy /y ..\10bit\Release\x265-static.lib x265-static_main10.lib
copy /y ..\12bit\Release\x265-static.lib x265-static_main12.lib
set EXTRA_LIBS="-DEXTRA_LIB=x265-static_main10.lib;x265-static_main12.lib"

cmake %CMAKE_ARGS% ..\source                     ^
    -DCMAKE_BUILD_TYPE=Release                   ^
    -DCMAKE_INSTALL_PREFIX=%LIBRARY_PREFIX%      ^
    -DENABLE_SHARED=TRUE                         ^
    -DLINKED_10BIT=ON                            ^
    -DLINKED_12BIT=ON                            ^
    -DEXTRA_LINK_FLAGS="-L."                     ^
    %EXTRA_LIBS%
if errorlevel 1 exit 1
cmake --build . --target install --config Release --parallel %CPU_COUNT%
if errorlevel 1 exit 1

del /Q /F %LIBRARY_PREFIX%\lib\x256-static.lib
