#!/bin/bash

app_dir="/home/django/dataradar"

screen -dmS django_app  sh -c "source $app_dir/venv/bin/activate; python $app_dir/manage.py runserver 0.0.0.0:8080; exec /bin/bash"
