#!/bin/bash

sudo yum install python-pip wget postgresql gcc python-devel postgresql-devel screen libxslt-devel nginx -y

app_dir="/home/ec2-user/feedcrunch"
user="ec2-user"

nginx_root="/etc/nginx/"
conf_files_root="/home/ec2-user/feedcrunch/codedeploy/Config_Files/"

sudo service nginx stop
sudo rm $nginx_root/nginx.conf || true
sudo rm $nginx_root/conf.d/feedcrunch.conf || true
sudo cp $conf_files_root/nginx.conf $nginx_root/nginx.conf
sudo cp $conf_files_root/feedcrunch.conf $nginx_root/conf.d/feedcrunch.conf
sudo chmod 777 -R /var/lib/nginx/
sudo service nginx start

virtualenv $app_dir/venv
source $app_dir/venv/bin/activate
pip install --upgrade pip
pip install -r $app_dir/requirements.txt

wget -q https://s3-eu-west-1.amazonaws.com/feedcrunch/codedeploy/data_crypt.zip -O $app_dir/fieldkeys/data.zip
sudo unzip -o $app_dir/fieldkeys/data.zip -d $app_dir/fieldkeys/
sudo chown -R $user:$user $app_dir/fieldkeys/

wget -q https://s3-eu-west-1.amazonaws.com/feedcrunch/codedeploy/data_env.zip -O $app_dir/data.zip
sudo unzip -o $app_dir/data.zip -d $app_dir/
sudo chown $user:$user $app_dir/.env

sudo chown -R $user:$user $app_dir
sudo chmod 755 -R $app_dir

#python $app_dir/manage.py collectstatic --noinput // Future use : Must run it manually.
chmod +x $app_dir/collectStatic.sh

python $app_dir/manage.py makemigrations
python $app_dir/manage.py migrate
python $app_dir/manage.py createcachetable
#python $app_dir/manage.py loaddata feedcrunch_dump.json
