DATARADAR.IO - DJANGO APP
====================

[![Build Status](https://travis-ci.com/DataIsTheNewBlack/FeedRadar.IO.svg?token=Mwzs9s5gJEGyrsnoybN5&branch=master)](https://travis-ci.com/DataIsTheNewBlack/FeedRadar.IO)
[![Coverage Status](https://coveralls.io/repos/github/DEKHTIARJonathan/django_starter_app/badge.svg?branch=master)](https://coveralls.io/github/DEKHTIARJonathan/django_starter_app?branch=master)
[![Dependency Status](https://gemnasium.com/badges/github.com/DataIsTheNewBlack/FeedRadar.IO.svg)](https://gemnasium.com/github.com/DataIsTheNewBlack/FeedRadar.IO)
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

## Travis with AWS CodeDeploy

You will need to set environment variables as followed:

| Key                    | Value                                                                                                    |
|------------------------|----------------------------------------------------------------------------------------------------------|
| TRAVIS                 | True                                                                                                     |
| DEBUG                  | True/False                                                                                               |
| SECRET_KEY             | '##############################################'                                                         |
| DATABASE_URL           | 'postgres://user:password@host:port/Database' (travis : 'postgres://postgres:@localhost:5432/travisci')  |
| CODECLIMATE_REPO_TOKEN | '##############################################'                                                         |
| AWS_ACCESS_KEY_ID      | '##############################################'                                                         |
| AWS_SECRET_ACCESS_KEY  | '##############################################'                                                         |