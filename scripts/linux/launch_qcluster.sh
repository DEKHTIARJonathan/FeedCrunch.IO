#!/bin/bash
cd ../..
source "venv/bin/activate"
exec python manage.py qcluster
