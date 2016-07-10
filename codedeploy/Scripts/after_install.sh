#!/bin/bash

sudo yum install python-pip wget postgresql gcc python-devel postgresql-devel screen libxslt-devel -y

app_dir="/home/ec2-user/feedcrunch"
image_dir="/home/ec2-user/images"
image_dest="/home/ec2-user/feedcrunch/"
user="ec2-user"

#Restoring all the saved profile pictures
sudo mv $image_dir $image_dest

virtualenv $app_dir/venv
source $app_dir/venv/bin/activate
pip install --upgrade pip
pip install -r $app_dir/requirements.txt

wget -q https://s3-eu-west-1.amazonaws.com/feedreader-codedeploy/feedreader_data/data_crypt.zip -O $app_dir/fieldkeys/data.zip
sudo unzip -o $app_dir/fieldkeys/data.zip -d $app_dir/fieldkeys/
sudo chown -R $user:$user $app_dir/fieldkeys/

wget -q https://s3-eu-west-1.amazonaws.com/feedreader-codedeploy/feedreader_data/data_env.zip -O $app_dir/data.zip
sudo unzip -o $app_dir/data.zip -d $app_dir/
sudo chown $user:$user $app_dir/.env

sudo chown -R $user:$user $app_dir
sudo chmod 755 -R $app_dir

python $app_dir/manage.py collectstatic --noinput
python $app_dir/manage.py makemigrations feedcrunch --noinput
python $app_dir/manage.py migrate --noinput
python $app_dir/manage.py loaddata feedcrunch_dump.json
