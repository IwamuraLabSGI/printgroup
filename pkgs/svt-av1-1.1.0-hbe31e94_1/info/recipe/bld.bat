@echo on

cd Build

cmake -G "NMake Makefiles"                           ^
      -DCMAKE_BUILD_TYPE=Release                     ^
      -DCMAKE_INSTALL_PREFIX:PATH="%LIBRARY_PREFIX%" ^
      -DCMAKE_INSTALL_LIBDIR="lib"                   ^
      -DBUILD_SHARED_LIBS=ON                         ^
      -DNATIVE=OFF                                   ^
      ..

if errorlevel 1 exit 1
nmake

if errorlevel 1 exit 1

nmake install
if errorlevel 1 exit 1
