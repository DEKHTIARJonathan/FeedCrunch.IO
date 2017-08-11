FeedCrunch.IO - DJANGO APP
====================
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
[![Build Status - Master](https://img.shields.io/travis/DEKHTIARJonathan/FeedCrunch.IO/master.svg?label=Travis%20-%20Master)](https://travis-ci.org/DEKHTIARJonathan/FeedCrunch.IO)
[![Build Status - Master](https://img.shields.io/travis/DEKHTIARJonathan/FeedCrunch.IO/dev.svg?label=Travis%20-%20Dev)](https://travis-ci.org/DEKHTIARJonathan/FeedCrunch.IO)
[![Dependency Status](https://beta.gemnasium.com/badges/github.com/DEKHTIARJonathan/FeedCrunch.IO.svg)](https://beta.gemnasium.com/projects/github.com/DEKHTIARJonathan/FeedCrunch.IO)
[![Coverage Status](https://coveralls.io/repos/github/DEKHTIARJonathan/FeedCrunch.IO/badge.svg)](https://coveralls.io/github/DEKHTIARJonathan/FeedCrunch.IO)
[![GitHub release](https://img.shields.io/github/release/DEKHTIARJonathan/FeedCrunch.IO.svg)](https://github.com/DEKHTIARJonathan/FeedCrunch.IO/releases)
[![ReadTheDocs](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat&maxAge=86400)](http://feedcrunch.readthedocs.io/en/latest/)
[![Website](https://img.shields.io/website-up-down-green-red/http/www.feedcrunch.io.svg?label=Feedcrunch.io)](https://www.feedcrunch.io)

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
