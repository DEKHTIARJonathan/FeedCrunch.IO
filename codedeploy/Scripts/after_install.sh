#!/bin/bash

sudo yum install python-pip wget postgresql gcc python-devel postgresql-devel screen libxslt-devel -y

app_dir="/home/ec2-user/feedcrunch"
user="ec2-user"

virtualenv $app_dir/venv
source $app_dir/venv/bin/activate
pip install --upgrade pip
pip install -r $app_dir/requirements.txt

wget -q https://s3-eu-west-1.amazonaws.com/feedreader-codedeploy/feedreader_data/data_.zip -O $app_dir/data.zip
sudo unzip -o $app_dir/data.zip -d $app_dir/
sudo chown $user:$user $app_dir/.env
sudo chmod 755 $app_dir/.env $app_dir/data.zip

python $app_dir/manage.py collectstatic --noinput
python $app_dir/manage.py makemigrations feedcrunch --noinput
python $app_dir/manage.py migrate --noinput
python $app_dir/manage.py manage.py load_data
