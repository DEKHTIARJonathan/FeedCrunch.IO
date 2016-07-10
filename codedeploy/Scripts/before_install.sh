#!/bin/bash

app_dir="/home/ec2-user/feedcrunch"
image_dir="/home/ec2-user/feedcrunch/images"
image_dest="/home/ec2-user/"
user="ec2-user"

#Saving all the profile pictures from the delete action
sudo mv $image_dir $image_dest

# Make directory for project
sudo rm -rf $app_dir
sudo rm -rf $app_dir
sudo mkdir -p $app_dir
sudo chown -R $user:$user $app_dir
sudo chmod -R 755 $app_dir
