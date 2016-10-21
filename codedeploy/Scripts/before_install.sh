#!/bin/bash

app_dir="/home/ec2-user/feedcrunch"
user="ec2-user"

#Saving all the profile pictures from the delete action

# Make directory for project
sudo rm -rf $app_dir
sudo mkdir -p $app_dir
sudo chown -R $user:$user $app_dir
sudo chmod -R 755 $app_dir
