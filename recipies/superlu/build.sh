#!/bin/bash

mkdir cbuild
cd cbuild

BUILD_CONFIG=Release

cmake .. \
    -DBUILD_SHARED_LIBS=true
    -DCMAKE_INSTALL_PREFIX=$PREFIX \
    -DCMAKE_BUILD_TYPE=%BUILD_CONFIG%

make -j ${CPU_COUNT}
make install
