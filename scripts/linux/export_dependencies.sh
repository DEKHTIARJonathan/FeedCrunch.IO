#!/bin/bash
cd ../..
source "venv/bin/activate"
pip freeze > requirements.txt
