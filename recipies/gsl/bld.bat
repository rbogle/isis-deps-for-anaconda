SET builddir=%SRC_DIR%\..\..\build_dir

rmdir /s /q %builddir%
if errorlevel 1 exit 1
mkdir  %builddir%
if errorlevel 1 exit 1
cd %builddir%
if errorlevel 1 exit 1

cmake %SRC_DIR% -G "NMake Makefiles" ^
                    -DCMAKE_BUILD_TYPE=Release ^
                    -DCMAKE_INSTALL_PREFIX=%LIBRARY_PREFIX% ^
                    -DBUILD_SHARED_LIBS=ON
if errorlevel 1 exit 1

cmake --build %builddir% --config Release --target install
if errorlevel 1 exit 1
