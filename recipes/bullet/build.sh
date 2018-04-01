#!/bin/bash

mkdir bullet-build
cd bullet-build
cmake .. -G "Unix Makefiles" -DINSTALL_LIBS=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=${PREFIX} -DCMAKE_INSTALL_RPATH=${PREFIX}
make -j ${CPU_COUNT}  || exit 1
make install
