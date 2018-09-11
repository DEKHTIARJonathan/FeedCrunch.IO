#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
"""
WSGI config for application project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application

platforms = ["TRAVIS", "HEROKU", "BLUEMIX"]


def load_env():
    """Get the path to the .env file and load it."""
    project_dir = os.path.dirname(os.path.dirname(__file__))
    dotenv.read_dotenv(os.path.join(project_dir, '.env'))


if not any(x in os.environ for x in platforms):
    load_env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")

application = get_wsgi_application()
