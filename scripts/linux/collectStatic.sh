#!/bin/bash
cd ../..

source venv/bin/activate

python $app_dir/manage.py collectstatic --noinput
