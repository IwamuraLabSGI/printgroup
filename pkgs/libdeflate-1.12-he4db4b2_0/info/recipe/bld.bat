@echo on

set C_INCLUDE_PATH=%LIBRARY_INC%

nmake /f Makefile.msc
if errorlevel 1 exit 1


:REM don't fail when making directories that might already exist
mkdir %LIBRARY_BIN%
mkdir %LIBRARY_LIB%
mkdir %LIBRARY_INC%

copy libdeflate.dll %LIBRARY_BIN%\libdeflate.dll
if errorlevel 1 exit 1
copy libdeflate.lib %LIBRARY_LIB%\libdeflate.lib
if errorlevel 1 exit 1
copy libdeflate.h   %LIBRARY_INC%\libdeflate.h
if errorlevel 1 exit 1
copy gzip.exe       %LIBRARY_BIN%\libdeflate-gzip.exe
if errorlevel 1 exit 1
copy gunzip.exe     %LIBRARY_BIN%\libdeflate-gunzip.exe
if errorlevel 1 exit 1
