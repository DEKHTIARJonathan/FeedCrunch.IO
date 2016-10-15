#!/bin/bash

NAME="feedcrunch_server"                                # Name of the application
DJANGODIR="/home/ec2-user/feedcrunch"                   # Django project directory
SOCKFILE="/home/ec2-user/feedcrunch/run/gunicorn.sock"  # we will communicte using this unix socket
USER="ec2-user"                                         # the user to run as
GROUP="ec2-user"                                        # the group to run as
NUM_WORKERS=3                                           # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE="application.settings"           # which settings file should Django use
DJANGO_WSGI_MODULE="application.wsgi"                   # WSGI module name
TIMEOUT=120                                             # Worker Timeout
KEEPALIVE=75

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
source $DJANGODIR/venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --keep-alive $KEEPALIVE \
  --timeout $TIMEOUT \
  --log-level=debug \
  --log-file=-
#  --bind=unix:$SOCKFILE \
#  --bind=127.0.0.1:8000 \
