FeedRadar.IO - DJANGO APP
====================

[![Build Status](https://travis-ci.com/DataIsTheNewBlack/FeedRadar.IO.svg?token=Mwzs9s5gJEGyrsnoybN5&branch=master)](https://travis-ci.com/DataIsTheNewBlack/FeedRadar.IO)
[![Dependency Status](https://gemnasium.com/badges/f7cb2bd2f6e6ccf302cab8638a30ce03.svg)](https://gemnasium.com/github.com/DataIsTheNewBlack/FeedRadar.IO)
[![Code Climate](https://codeclimate.com/repos/5763ac50e58714007d008297/badges/5c16f9f102cc95935231/gpa.svg)](https://codeclimate.com/repos/5763ac50e58714007d008297/feed)
[![Test Coverage](https://codeclimate.com/repos/5763ac50e58714007d008297/badges/5c16f9f102cc95935231/coverage.svg)](https://codeclimate.com/repos/5763ac50e58714007d008297/coverage)
[![Issue Count](https://codeclimate.com/repos/5763ac50e58714007d008297/badges/5c16f9f102cc95935231/issue_count.svg)](https://codeclimate.com/repos/5763ac50e58714007d008297/feed)

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
