FeedCrunch.IO - DJANGO APP
====================

[![Build Status](https://travis-ci.com/DataIsTheNewBlack/FeedCrunch.IO.svg?token=Mwzs9s5gJEGyrsnoybN5&branch=master)](https://travis-ci.com/DataIsTheNewBlack/FeedCrunch.IO)
[![Dependency Status](https://gemnasium.com/badges/github.com/DataIsTheNewBlack/FeedCrunch_Dependencies.svg)](https://gemnasium.com/github.com/DataIsTheNewBlack/FeedCrunch_Dependencies)
[![Code Climate](https://codeclimate.com/repos/5772aa87f97096006f001cb4/badges/7ea6335aee9b44fcdc67/gpa.svg)](https://codeclimate.com/repos/5772aa87f97096006f001cb4/feed)
[![Test Coverage](https://codeclimate.com/repos/5772aa87f97096006f001cb4/badges/7ea6335aee9b44fcdc67/coverage.svg)](https://codeclimate.com/repos/5772aa87f97096006f001cb4/coverage)
[![Issue Count](https://codeclimate.com/repos/5772aa87f97096006f001cb4/badges/7ea6335aee9b44fcdc67/issue_count.svg)](https://codeclimate.com/repos/5772aa87f97096006f001cb4/feed)

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

| Key                      | Value                                                                                                    |
|--------------------------|----------------------------------------------------------------------------------------------------------|
| TRAVIS                   | True                                                                                                     |
| DEBUG                    | True/False                                                                                               |
| SECRET_KEY               | '##############################################'                                                         |
| DATABASE_URL             | 'postgres://user:password@host:port/Database'<br>(travis: 'postgres://postgres:@localhost:5432/travisci')|
| CODECLIMATE_REPO_TOKEN   | '##############################################'                                                         |
| AWS_ACCESS_KEY_ID        | '##############################################'	                                                        |
| AWS_SECRET_ACCESS_KEY    | '##############################################'                                                         |


Options needed to be declared in the Admin Panel :

| Key                      | Value                                            |
|--------------------------|--------------------------------------------------|
| twitter_consumer_secret  | '##############################################' |
| twitter_consumer_key     | '##############################################' |
| mailchimp_client_secret  | '##############################################' |
| mailchimp_client_id      | '##############################################' |
| freemium_period          | True/False                                       |
