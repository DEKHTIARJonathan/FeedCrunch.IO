DATARADAR.IO - DJANGO APP
====================

[![Build Status](https://travis-ci.org/DEKHTIARJonathan/django_starter_app.svg?branch=master)](https://travis-ci.org/DEKHTIARJonathan/django_starter_app)
[![Coverage Status](https://coveralls.io/repos/github/DEKHTIARJonathan/django_starter_app/badge.svg?branch=master)](https://coveralls.io/github/DEKHTIARJonathan/django_starter_app?branch=master)
[![Dependency Status](https://gemnasium.com/badges/github.com/DEKHTIARJonathan/django_starter_app.svg)](https://gemnasium.com/github.com/DEKHTIARJonathan/django_starter_app)
[![Code Climate](https://codeclimate.com/github/DEKHTIARJonathan/django_starter_app/badges/gpa.svg)](https://codeclimate.com/github/DEKHTIARJonathan/django_starter_app)
[![Test Coverage](https://codeclimate.com/github/DEKHTIARJonathan/django_starter_app/badges/coverage.svg)](https://codeclimate.com/github/DEKHTIARJonathan/django_starter_app/coverage)
[![Issue Count](https://codeclimate.com/github/DEKHTIARJonathan/django_starter_app/badges/issue_count.svg)](https://codeclimate.com/github/DEKHTIARJonathan/django_starter_app)

## Installation

Rename the file ".env.dist" to ".env"
```sh
mv .env.dist .env
```

Then please update the file ".env" with the correct values.

If needed, you can generate a secret key for DJANGO here: http://www.miniwebtool.com/django-secret-key-generator/

```sh
pip install virtualenv
virtualenv venv

## Windows
venv\Scripts\activate.bat

## Linux
source venv/bin/activate

pip install -r requirements.txt
```

## Launching Server

```sh
python manage.py runserver 0.0.0.0:5000
```

Launching Tests

```sh
coverage run manage.py test
coverage report -m
coverage html
```

## Travis / Heroku

You will need to set environment variables as followed:

| Key                                    | Value                                            |
|----------------------------------------|--------------------------------------------------|
| TRAVIS/HEROKU (if needed)              | True                                             |
| DEBUG                                  | True/False                                       |
| SECRET_KEY                             | '##############################################' |
| DATABASE_URL (not needed for travis)   | 'postgres://user:password@host:port/Database'    |
| CODECLIMATE_REPO_TOKEN                 | '##############################################' |
