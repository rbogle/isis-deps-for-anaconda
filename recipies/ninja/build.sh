#!/bin/bash

if [[ $(uname) == MINGW* ]]; then
  PREFIX="${PREFIX}"/Library/mingw-w64
  BUILD_ARGS="--host=mingw --platform=mingw"
fi

./configure.py --bootstrap --verbose ${BUILD_ARGS}

cp -p ninja "${PREFIX}/bin/ninja"