#!/bin/bash

app_dir="/home/ec2-user/dataradar"

# Make directory for project
rm -rf $app_dir
mkdir -p $app_dir
chown -R django:django $app_dir
chmod -R 755 $app_dir
