setlocal enableextensions enabledelayedexpansion

:: Trailing semicolon in this variable as set by current (2017/01)
:: conda-build breaks us. Manual fix:
set "MSYS2_ARG_CONV_EXCL=/AI;/AL;/OUT;/out"

:: Setting variables in Cygwin style.
set LIBRARY_INC_CW=!LIBRARY_INC:\=/!
set LIBRARY_INC_CW=!LIBRARY_INC_CW::=!
set LIBRARY_INC_CW=/%LIBRARY_INC_CW%

set LIBRARY_LIB_CW=!LIBRARY_LIB:\=/!
set LIBRARY_LIB_CW=!LIBRARY_LIB_CW::=!
set LIBRARY_LIB_CW=/%LIBRARY_LIB_CW%

:: Compiling.
make -f Makefile.win32 CFG=release ^
  PIXMAN_CFLAGS=-I%LIBRARY_INC_CW%/pixman ^
  PIXMAN_LIBS=%LIBRARY_LIB_CW%/pixman-1.lib ^
  ZLIB_CFLAGS=-I%LIBRARY_INC_CW% ^
  LIBPNG_CFLAGS=-I%LIBRARY_INC_CW% ^
  CAIRO_LIBS='gdi32.lib msimg32.lib user32.lib %LIBRARY_LIB_CW%/libpng.lib %LIBRARY_LIB_CW%/zlib.lib %LIBRARY_LIB_CW%/freetype.lib %LIBRARY_LIB_CW%/fontconfig.lib'
if errorlevel 1 exit 1
pushd util\cairo-gobject
make -f Makefile.win32 CFG=release ^
  PIXMAN_CFLAGS=-I%LIBRARY_INC_CW%/pixman ^
  PIXMAN_LIBS=%LIBRARY_LIB_CW%/pixman-1.lib ^
  ZLIB_CFLAGS=-I%LIBRARY_INC_CW% ^
  LIBPNG_CFLAGS=-I%LIBRARY_INC_CW% ^
  GOBJECT_CFLAGS='-I%LIBRARY_INC_CW%/glib-2.0 -I%LIBRARY_LIB_CW%/glib-2.0/include' ^
  GOBJECT_LIBS='%LIBRARY_LIB_CW%/glib-2.0.lib %LIBRARY_LIB_CW%/gobject-2.0.lib'
if errorlevel 1 exit 1
popd

:: Installing.
set CAIRO_INC=%LIBRARY_INC%\cairo
mkdir %CAIRO_INC%
move cairo-version.h %CAIRO_INC%
move src\cairo-features.h %CAIRO_INC%
move src\cairo.h %CAIRO_INC%
move src\cairo-deprecated.h %CAIRO_INC%
move src\cairo-win32.h %CAIRO_INC%
move src\cairo-script.h %CAIRO_INC%
move src\cairo-ps.h %CAIRO_INC%
move src\cairo-pdf.h %CAIRO_INC%
move src\cairo-svg.h %CAIRO_INC%
move src\cairo-ft.h %CAIRO_INC%
move util\cairo-gobject\cairo-gobject.h %CAIRO_INC%

move src\release\cairo.dll %LIBRARY_BIN%
move src\release\cairo.lib %LIBRARY_LIB%
move src\release\cairo-static.lib %LIBRARY_LIB%
move util\cairo-gobject\release\cairo-gobject.dll %LIBRARY_BIN%
move util\cairo-gobject\release\cairo-gobject.lib %LIBRARY_LIB%

for %%F in (pc-files\*.pc) do (
  envsubst '${LIBRARY_PREFIX}${PKG_VERSION}' < %%F > %LIBRARY_LIB%\pkgconfig\%%~nF.pc
)
