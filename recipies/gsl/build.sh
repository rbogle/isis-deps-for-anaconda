#!/bin/bash

./configure --prefix=$PREFIX

make
make check
make install

if [ "$(uname)" == "Darwin" ]
then
    rm "$PREFIX"/lib/libgslcblas.*
    ln -s "$PREFIX/lib/libopenblas.dylib" "$PREFIX/lib/libgslcblas.dylib"
    ln -s "$PREFIX/lib/libopenblas.dylib" "$PREFIX/lib/libgslcblas.0.dylib"
elif [ "$(uname)" == "Linux" ]
then
    rm "$PREFIX"/lib/libgslcblas.*
    ln -s "$PREFIX/lib/libopenblas.so" "$PREFIX/lib/libgslcblas.so"
    ln -s "$PREFIX/lib/libopenblas.so" "$PREFIX/lib/libgslcblas.so.0"
fi

