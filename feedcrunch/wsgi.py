"""
WSGI config for {{ project_name }} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/wsgi/
"""

from __future__ import unicode_literals

import os
import sys

from django.core.wsgi import get_wsgi_application

import dotenv

def load_env():
    "Get the path to the .env file and load it."
    project_dir = os.path.dirname(os.path.dirname(__file__))
    dotenv.read_dotenv(os.path.join(project_dir, '.env'))
	
load_env()
	
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")

application = get_wsgi_application()