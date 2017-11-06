#!/bin/bash

# build already exists
mkdir cbuild
cd cbuild

BUILD_CONFIG=Release

# On OSX, we need to ensure we're using conda's gcc/g++
if [[ `uname` == Darwin ]]; then
    export CC=gcc
    export LD=gcc
    export CXX=g++
fi

cmake .. \
    -Wno-dev \
	-DCMAKE_INSTALL_PREFIX=$PREFIX \
    -DCMAKE_BUILD_TYPE=%BUILD_CONFIG% 

make -j"$(($(nproc)  - 2))" all
make install
