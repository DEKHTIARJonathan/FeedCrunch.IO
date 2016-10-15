#!/bin/bash

app_dir="/home/ec2-user/feedcrunch"

screen -dmS django_app  sh -c "source $app_dir/venv/bin/activate; $app_dir/gunicorn.sh ; exec /bin/bash"
