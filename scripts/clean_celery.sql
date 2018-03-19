delete from celery_monitor_taskstate where 1=1;
delete from celery_monitor_workerstate where 1=1;
delete from django_celery_beat_periodictask where 1=1;
delete from django_celery_beat_periodictasks where 1=1;
delete from django_celery_beat_intervalschedule where 1=1;
delete from django_celery_beat_crontabschedule where 1=1;
delete from django_celery_beat_solarschedule where 1=1;