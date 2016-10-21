#!/bin/bash

ScreenName="django_app"
if screen -list | grep -q $ScreenName; then
    screen -X -S $ScreenName quit
fi

FILE="/home/ec2-user/feedcrunch/run/gunicorn.pid"
if [ -f $FILE ]; then
   echo "File '$FILE' Exists"
   kill -9 `cat $FILE`
fi
