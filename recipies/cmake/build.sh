#!/bin/sh

if [[ ${HOST} =~ .*darwin.* ]]; then
  export LDFLAGS=${LDFLAGS_CC}
fi

./bootstrap \
             --prefix="${PREFIX}" \
             --system-libs \
             --no-qt-gui \
             --no-system-libarchive \
             --no-system-jsoncpp \
             --parallel=${CPU_COUNT} \
             -- \
             -DCMAKE_FIND_ROOT_PATH="${PREFIX}" \
             -DCMAKE_INSTALL_RPATH="${PREFIX}/lib" \
             -DCMAKE_CXX=${CXX} \
             -DCMAKE_CC=${CC} \
             -DCMAKE_BUILD_TYPE:STRING=Release
make install -j${CPU_COUNT} ${VERBOSE_CM}
