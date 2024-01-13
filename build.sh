#!/bin/bash
echo " hurricane build tool "
echo "======================"

echo "[hbt] compiling dialouge with mads..."
cd assets/dialouge
python3.10 mads.zip -i main.mds -o ../npcs.json
cd ../..
echo "[hbt] done"

echo "[hbt] compiling assets.dat..."
python3 makeassets.py
echo "[hbt] done"

echo "[hbt] getting version..."
python3 -c "from hurricane.const import VERSION;f = open('VERSION', 'w');f.write(str(VERSION)[1:])"
version="$(cat VERSION)"
echo "[hbt] done, version ${version}"

echo "[hbt] checking version ${version}..."
if [ -f "dist/Hurricane-${version}-py38-none-any.whl" ]; then
  echo "[hbt] done, this release has already been build"
  echo "[hbt] cleaning up..."
  rm VERSION
  echo "[hbt] done, assets + npcs built but hurricane did NOT compleate sucessfully"
  exit 0
fi
echo "[hbt] done, build is cleared"


echo "[hbt] zipping source code..."
cd hurricane
zip -r "../dist/Hurricane-${version}-py38.zip" * -x "*.pyc" -9 -r
cd ..
echo "[hbt] done"

echo "[hbt] building wheel file"
python3 setup.py bdist_wheel
echo "[hbt] done"

echo "[hbt] cleaning up..."
rm VERSION
echo "[hbt] done, hurricane version ${version} sucessfully built"