#!/bin/bash

sudo yum install python-pip wget postgresql gcc python-devel postgresql-devel screen -y
pip install --upgrade pip

rm -rf /dataradar/venv
virtualenv /dataradar/venv
source /dataradar/venv/bin/activate
pip install --upgrade pip

pip install -r /dataradar/requirements.txt

wget -q https://s3-eu-west-1.amazonaws.com/feedreader-codedeploy/feedreader_data/data_.zip- O /dataradar/data.zip
unzip -o data.zip
python /dataradar/manage.py collectstatic --noinput
python /dataradar/manage.py migrate --noinput
python /dataradar/manage.py makemigrations --noinput
