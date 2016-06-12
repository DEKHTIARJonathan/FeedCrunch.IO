#!/bin/bash

sudo yum install python-pip wget postgresql gcc python-devel postgresql-devel screen -y

app_dir="/home/ec2-user/dataradar"

rm -rf $app_dir/venv
virtualenv $app_dir/venv
source $app_dir/venv/bin/activate
pip install --upgrade pip

pip install -r $app_dir/requirements.txt
sudo wget -q https://s3-eu-west-1.amazonaws.com/feedreader-codedeploy/feedreader_data/data_.zip -O $app_dir/data.zip
sudo unzip -o $app_dir/data.zip
sudo python $app_dir/manage.py collectstatic --noinput
sudo python $app_dir/manage.py migrate --noinput
sudo python $app_dir/manage.py makemigrations --noinput
