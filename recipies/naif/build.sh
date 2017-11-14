#!/bin/base_path
mkdir -p ${PREFIX}/lib/naif
mkdir -p ${PREFIX}/include/naif
mkdir -p ${PREFIX}/doc/naif

if [ -d ./cspice ]; then
	cd ./cspice
fi

cp ./lib/*.a ${PREFIX}/lib/naif/
cp ./include/*.h ${PREFIX}/include/naif/
cp ./exe/* ${PREFIX}/bin/
cp -r ./doc/* ${PREFIX}/doc/naif
