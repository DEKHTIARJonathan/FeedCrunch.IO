#!/bin/bash

screen -dmS django_app  sh -c "source /dataradar/venv/bin/activate; python /dataradar/manage.py runserver 0.0.0.0:8080; exec /bin/bash"

