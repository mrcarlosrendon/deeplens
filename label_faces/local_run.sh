#!/bin/bash

rm -rf build
mkdir build
cp *.py build
python -m pip install -t build -r requirements.txt
unzip -d build python_sdk_1_0_0.zip
cd build
AWS_IOT_THING_NAME=deeplens_4617be20-509f-4a5d-ae36-3dd0f5ba766c time python label_faces.py
cd ..
