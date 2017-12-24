SET AWS_DEFAULT_REGION=us-east-1
rmdir /S /Q build
mkdir build
copy *.py build
copy /Y ..\rekognition_demos\describe_image.py build\describe_image.py
python -m pip install -t build -r requirements.txt
"c:\Program Files\7-Zip\7z.exe" x python_sdk_1_0_0.zip -obuild -y
del build.zip
cd build
"c:\Program Files\7-Zip\7z.exe" a build.zip *
move build.zip ..
cd ..
aws lambda update-function-code --function-name label-faces --zip-file fileb://build.zip --publish

