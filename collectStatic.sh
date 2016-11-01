#!/bin/bash

app_dir="/home/ec2-user/feedcrunch"

source $app_dir/venv/bin/activate

python $app_dir/manage.py collectstatic --noinput
