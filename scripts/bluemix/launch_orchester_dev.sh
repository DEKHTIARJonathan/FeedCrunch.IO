#!/bin/bash

celery beat -A application --loglevel=debug --detach 
celery events -A application --loglevel=debug --camera=django_celery_monitor.camera.Camera --frequency=2.0 --detach
celery worker -A application --loglevel=debug --events