#!/bin/bash
cd ../..
source "venv/bin/activate"
pip install --upgrade pip
pip install "lib_bin/linux/scipy-0.18.1-cp27-cp27mu-manylinux1_x86_64.whl"
pip install -r requirements.txt
