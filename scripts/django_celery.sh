# launch Worker
celery worker -A application -l debug --events

# launch heartbeat
celery beat -A application --loglevel=debug

# launch camera 
celery events -A application --loglevel=debug --camera=django_celery_monitor.camera.Camera --frequency=2.0