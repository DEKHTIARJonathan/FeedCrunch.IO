#!/usr/bin/env python
import os
import sys

import dotenv

if __name__ == "__main__":

	platforms = ["TRAVIS", "HEROKU"]
	if not any(x in os.environ for x in platforms):
		dotenv.read_dotenv()

	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")

	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)
