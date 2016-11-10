#!/bin/bash

ScreenName1="django_app"
ScreenName2="QCluster_app"

if screen -list | grep -q $ScreenName1; then
    screen -X -S $ScreenName1 quit
fi

if screen -list | grep -q $ScreenName2; then
    screen -X -S $ScreenName2 quit
fi

FILE="/home/ec2-user/feedcrunch/run/gunicorn.pid"
if [ -f $FILE ]; then
   echo "File '$FILE' Exists"
   kill -9 `cat $FILE`
fi
