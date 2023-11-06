#!/usr/bin/env bash
# Makes a portable executable for the snake game
if [ -d "build" ]; then
    rm -rf "build"
fi

if [ -d "dist" ]; then
    rm -rf "dist"
fi

if [ -f "main.spec" ]; then
    rm "main.spec"
fi

python -m venv build
. ./build/bin/activate
python -m pip install -r requirements.txt
pyinstaller main.py
echo "Jobs done!"
