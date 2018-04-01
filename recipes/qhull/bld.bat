rem build already exists
mkdir cbuild
cd cbuild

set BUILD_CONFIG=Release

:: tell cmake where Python is
set PYTHON_LIBRARY=%PREFIX:\=/%/libs/python%PY_VER:~0,1%%PY_VER:~2,1%.lib


set CC=cl.exe

rem cmake .. -G "Ninja" ^
rem cmake .. -LAH -G "%CMAKE_GENERATOR%" ^
cmake .. -LAH -G "NMake Makefiles" ^
    -Wno-dev ^
    -DCMAKE_BUILD_TYPE=%BUILD_CONFIG% ^
    -DCMAKE_INSTALL_PREFIX:PATH="%LIBRARY_PREFIX:\=/%"

if errorlevel 1 exit 1

rem ninja install
cmake --build . --target INSTALL --config %BUILD_CONFIG%
if errorlevel 1 exit 1
