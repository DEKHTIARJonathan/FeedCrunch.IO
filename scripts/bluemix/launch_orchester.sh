#!/bin/bash

celery beat -A application --loglevel=info --detach 
celery events -A application --loglevel=info --camera=django_celery_monitor.camera.Camera --frequency=2.0 --detach
celery worker -A application -l info --events