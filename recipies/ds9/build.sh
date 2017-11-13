#!/bin/bash

if [ $(uname) == Darwin ]; then
  sed -i '' '/codesign/d' ./ds9/unix/Makefile.in
fi

./unix/configure --prefix $PREFIX
make
