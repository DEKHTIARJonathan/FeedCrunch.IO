#!/bin/bash

app_dir="/home/ec2-user/feedcrunch"

screen -dmS django_app  sh -c "source $app_dir/venv/bin/activate; gunicorn feedcrunch.wsgi:application --bind 0.0.0.0:8080; exec /bin/bash"
