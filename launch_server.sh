#!/bin/bash

if [ -z "$VCAP_APP_PORT" ];
  then SERVER_PORT=5000;
  else SERVER_PORT="$VCAP_APP_PORT";
fi

pip uninstall django-material -y
pip install https://github.com/hairychris/django-material/archive/2b3d70347cf29bcc02b06d3319f9617b626502c8.zip

echo [$0] port is------------------- $SERVER_PORT
python manage.py makemigrations feedcrunch
python manage.py migrate
python manage.py createcachetable
#echo "from django.contrib.auth.models import User; User.objects.create_superuser('${USER}', '${MAIL}', '${PASS}')" | python manage.py shell

echo [$0] Starting Django Server... 
#python manage.py runserver 0.0.0.0:$SERVER_PORT --noreload

NAME="FeedCrunch_Server"                                # Name of the application
NUM_WORKERS=3                                           # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE="application.settings"           # which settings file should Django use
DJANGO_WSGI_MODULE="application.wsgi"                   # WSGI module name
TIMEOUT=120                                             # Worker Timeout
KEEPALIVE=75                                            # Keep Alive Timer


# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --keep-alive $KEEPALIVE \
  --timeout $TIMEOUT 