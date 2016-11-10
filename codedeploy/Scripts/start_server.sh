#!/bin/bash

app_dir="/home/ec2-user/feedcrunch"

ScreenName1="django_app"
ScreenName2="QCluster_app"

screen -dmS $ScreenName1 sh -c "source $app_dir/venv/bin/activate; $app_dir/gunicorn.sh ; exec /bin/bash"
screen -dmS $ScreenName2 sh -c "source $app_dir/venv/bin/activate; python manage.py qcluster; exec /bin/bash"
