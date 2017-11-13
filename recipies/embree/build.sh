#!/bin/bash
set -e
cd lib
if [ ! -f "libembree${SHLIB_EXT}" ]
then
  ln -s libembree.so libembree${SHLIB_EXT}
fi
cd ..
mkdir -p ${PREFIX}/bin
mkdir -p ${PREFIX}/lib
mkdir -p ${PREFIX}/include
mkdir -p ${PREFIX}/doc/embree

cp -rv ./bin/* ${PREFIX}/bin/
cp -rv ./lib/* ${PREFIX}/lib/
cp -rv ./include/* ${PREFIX}/include/
cp -rv ./doc/* ${PREFIX}/doc/embree/
