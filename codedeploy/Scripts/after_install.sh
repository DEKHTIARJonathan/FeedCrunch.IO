#!/bin/bash

sudo yum install python-pip wget postgresql gcc python-devel postgresql-devel screen -y

app_dir="/home/django/dataradar"

virtualenv $app_dir/venv
source $app_dir/venv/bin/activate
pip install --upgrade pip
pip install -r $app_dir/requirements.txt

wget -q https://s3-eu-west-1.amazonaws.com/feedreader-codedeploy/feedreader_data/data_.zip -O $app_dir/data.zip
unzip -o $app_dir/data.zip
python $app_dir/manage.py collectstatic --noinput
python $app_dir/manage.py migrate --noinput
python $app_dir/manage.py makemigrations --noinput
