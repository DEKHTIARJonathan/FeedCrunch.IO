#!/bin/bash

celery beat -A application --loglevel=debug --detach --logfile=celerybeat.log
celery events -A application --loglevel=debug --camera=django_celery_monitor.camera.Camera --frequency=2.0 --detach --logfile=celeryevents.log
celery worker -A application -l debug --events --logfile=celeryworker.log