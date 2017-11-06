#!/bin/bash
set -e
cd lib
if [ ! -f "libembree${SHLIB_EXT}" ]
then
  ln -s libembree.so libembree${SHLIB_EXT}
fi
cd ..
cp -rv * "${PREFIX}"
