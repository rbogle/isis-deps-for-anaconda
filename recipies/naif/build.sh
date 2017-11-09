#!/bin/base_path
mkdir -p ${PREFIX}/lib/naif
mkdir -p ${PREFIX}/include/naif
mkdir -p ${PREFIX}/doc/naif

cp cspice/lib/*.a ${PREFIX}/lib/naif/
cp cspice/include/*.h ${PREFIX}/include/naif/
cp cspice/exe/* ${PREFIX}/bin/
cp -r cspice/doc/* ${PREFIX}/doc/naif
