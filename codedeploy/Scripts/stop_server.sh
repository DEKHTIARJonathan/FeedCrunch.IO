#!/bin/bash

screen -X -S django_app quit
kill -9 `cat /home/ec2-user/feedcrunch/run/gunicorn.pid`
