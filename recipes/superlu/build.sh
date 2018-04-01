#!/bin/bash

mkdir cbuild
cd cbuild

BUILD_CONFIG=Release

# Enable building shared libraries
# Disable the Fortan interface
#   - By default it is enabled, which requires the meta.yaml.tmpl to include
#     gfortran_linux-x64 (via anaconda channel).
#     This was causing an ld cannot find -lgomp error.
cmake .. \
    -DBUILD_SHARED_LIBS=TRUE \
    -DXSDK_ENABLE_Fortran=FALSE \
    -DCMAKE_INSTALL_PREFIX=$PREFIX \
    -DCMAKE_BUILD_TYPE=%BUILD_CONFIG%

make -j ${CPU_COUNT}
make install
