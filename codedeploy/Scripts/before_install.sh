#!/bin/bash

app_dir="/home/ec2-user/dataradar"

# Make directory for project
sudo rm -rf $app_dir
sudo mkdir -p $app_dir
sudo chown -R django:django $app_dir
sudo chmod -R 755 $app_dir
