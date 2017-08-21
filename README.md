FeedCrunch.IO - Empower RSS feeds to a whole new level
======================================================

[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
[![license](https://img.shields.io/github/license/DEKHTIARJonathan/FeedCrunch.IO.svg)](https://opensource.org/licenses/GPL-3.0/)
[![GitHub release](https://img.shields.io/github/release/DEKHTIARJonathan/FeedCrunch.IO.svg)](https://github.com/DEKHTIARJonathan/FeedCrunch.IO/releases)
[![ReadTheDocs](https://img.shields.io/badge/docs-latest-brightgreen.svg?style=flat&maxAge=86400&label=documentation)](http://feedcrunch.readthedocs.io/en/latest/)
[![Twitter Follow](https://img.shields.io/twitter/follow/born2data.svg?style=flat&label=Follow%20me:%20@born2data)](https://twitter.com/intent/user?screen_name=born2data)

__________________
Production Metrics<br>
[![Build Status - Master](https://img.shields.io/travis/DEKHTIARJonathan/FeedCrunch.IO/master.svg?label=Travis%20-%20Master)](https://travis-ci.org/DEKHTIARJonathan/FeedCrunch.IO)
[![Updates](https://pyup.io/repos/github/DEKHTIARJonathan/FeedCrunch.IO/shield.svg)](https://pyup.io/repos/github/DEKHTIARJonathan/FeedCrunch.IO/)
[![Python 3](https://pyup.io/repos/github/DEKHTIARJonathan/FeedCrunch.IO/python-3-shield.svg)](https://pyup.io/repos/github/DEKHTIARJonathan/FeedCrunch.IO/)
[![Coverage Status](https://img.shields.io/coveralls/DEKHTIARJonathan/FeedCrunch.IO/master.svg?label=coveralls)](https://coveralls.io/github/DEKHTIARJonathan/FeedCrunch.IO?branch=master)
[![codecov](https://img.shields.io/codecov/c/github/DEKHTIARJonathan/FeedCrunch.IO/master.svg?label=codecov)](https://codecov.io/gh/DEKHTIARJonathan/FeedCrunch.IO)
[![Website](https://img.shields.io/website-up-down-green-red/http/www.feedcrunch.io.svg?label=Feedcrunch.io)](https://www.feedcrunch.io)
__________________
Development Metrics<br>
[![Build Status - Dev](https://img.shields.io/travis/DEKHTIARJonathan/FeedCrunch.IO/dev.svg?label=Travis%20-%20Dev)](https://travis-ci.org/DEKHTIARJonathan/FeedCrunch.IO)
[![Coverage Status](https://img.shields.io/coveralls/DEKHTIARJonathan/FeedCrunch.IO/dev.svg?label=coveralls)](https://coveralls.io/github/DEKHTIARJonathan/FeedCrunch.IO?branch=master)
[![Codecov Status](https://img.shields.io/codecov/c/github/DEKHTIARJonathan/FeedCrunch.IO/dev.svg?label=codecov)](https://codecov.io/gh/DEKHTIARJonathan/FeedCrunch.IO)
[![Website](https://img.shields.io/website-up-down-green-red/http/feedcrunch-dev.eu-gb.mybluemix.net.svg?label=Feedcrunch.io%20-%20Dev)](https://feedcrunch-dev.eu-gb.mybluemix.net/)

# Issues

Feel free to submit issues and enhancement requests.

# Contributing guidelines

Please have a look to the [Contributing Guidelines](CONTRIBUTING.md) first.

We follow the "fork-and-pull" Git workflow.

1. **Fork** the repo on GitHub
2. **Clone** the project to your own machine
3. **Commit** changes to your own branch
4. **Push** your work back up to your fork
5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!

# Copyright and Licensing

The project is released under the GNU Affero General Public License v3.0, which gives you the following rights in summary:

|**Permissions**  |**Limitations** |**Conditions**                 |
|---------------- |--------------- |------------------------------ |
|*Commercial use* |*Liability*     |*License and copyright notice* |
|*Distribution*   |*Warranty*      |*Disclose source*              |
|*Modification*   |                |*Network use is distribution*  |
|*Patent use*     |                |*Same license*                 |
|*Private use*    |                |*State changes*                |

## 1. How to Install the development server

### 1.1. Create and launch the databases servers

#### 1.1.1 Create a PostgreSQL database

#### 1.1.2 Create a RabbitMQ database

### 1.2. Install Python 3.6

To my opinion, the Python distribution from Continuum Analytics Anaconda is an **absolute go-to**: https://www.continuum.io/downloads.
You can download this version and install it.

### 1.3. Rename the file ".env.dist" to ".env"

```sh
mv .env.dist .env
```

### 1.4. Update the values inside the .env files with the correct values.

- **DATABASE_URL:** Format the PostgreSQL credentials as followed: *postgres://user:password@server:port/dbname*
- **RABBITMQ_URL:** Format the RabbitMQ credentials as followed: *amqp://username:password@server:port/instance_name*
- **SECRET_KEY:** Django needs a secret key to operate securely, you can generate one here: [Secret Key Generator](http://www.miniwebtool.com/django-secret-key-generator/)
- **DEBUG:** True/False. Absolutely needs to be at *False* to put into production.
- **AWS_USER:** See documentation from AWS, it needs to have rights for SES (emails) and S3 (storage).
- **AWS_SECRET_KEY:** See documentation from AWS, it needs to have rights for SES (emails) and S3 (storage).
- **EMAIL_DEFAULT_SENDER:** The email used when the platform send emails to customers
- **FIELD_ENCRYPTION_KEY** The encryption key used to encrypt hashes and API Keys inside the database, can be generated with the command: *python manage.py generate_encryption_key*

### 1.5. Install the dependencies

#### 1.5.1. Linux / Mac Os
```sh
pip install virtualenv
virtualenv venv

source venv/bin/activate

pip install -r requirements.txt
```

#### 1.5.2. Windows
```sh
pip install virtualenv
virtualenv venv

venv\Scripts\activate.bat

scripts\win\install_dependencies_py36.bat
```

### 1.6. Migrate the database to the server.
```sh
# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

# Then
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable
python manage.py loaddata feedcrunch_dump.json # This operation loads fixtures in the database and can take a few minutes.
```

### 1.7. Create a superuser on the application.

```sh
# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

# Then
python manage.py createsuperuser # Fill in your information
```

### 1.8. Set the application options

Once installed, the application needs a few parameters to manage the behaviour of the platform.

Please access the following address and login with the superuser account created before: *(http|https)://server-ip:port/admin/*
Once logged-in, you need to open the **Options** setting under **Feedcrunch**.

If not created, the following settings need to be created. Else, you can just modify the value accordingly to your needs.

- **display_user_count:** (Default: False) Control if the application shows in the footer the number of post (False) or subscribed users (True).
- **freemium_period:** (Default: False) Control if the application run in freemium or normal (not implemented yet, only freemium supported).
- **max_articles_on_interest_sub:** (Default: 5) Maximum of old RSS Posts added when a user add an interest during onboarding.
- **max_recommendations:** (Default: 100) Maximum of recommendations made to user on the recommendation pane.
- **max_rss_posts:** (Default: 25) Maximum of old RSS Posts added when a user subscribe to a new RSS Feed.
- **facebook_app_id:** Can be obtained on the Facebook developer platform: <https://developers.facebook.com/>
- **facebook_app_secret**  Can be obtained on the Facebook developer platform: <https://developers.facebook.com/>
- **linkedin_client_id:** Can be obtained on the LinkedIn developer platform: <https://developer.linkedin.com/>
- **linkedin_client_secret:** Can be obtained on the LinkedIn developer platform: <https://developer.linkedin.com/>
- **mailchimp_client_id:** Can be obtained on the Mailchimp developer platform: <https://developer.mailchimp.com/>
- **mailchimp_client_secret:** Can be obtained on the Mailchimp developer platform: <https://developer.mailchimp.com/>
- **slack_client_id:** Can be obtained on the Slack developer platform: <https://slack.com/developers>
- **slack_client_secret:** Can be obtained on the Slack developer platform: <https://slack.com/developers>
- **twitter_consumer_key:** Can be obtained on the Twitter developer platform: <https://dev.twitter.com/>
- **twitter_consumer_secret:** Can be obtained on the Twitter developer platform: <https://dev.twitter.com/>

## 2. How to launch the development server

```sh
# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

# Then
python manage.py runserver 0.0.0.0:5000 # Launch the server accessible from the LAN on the port 5000 at the IP-Address of the server.
```

## 3. How to launch unit tests

```sh
# Linux
source venv/bin/activate

# Windows
venv\Scripts\activate.bat

# Then
coverage run manage.py test
coverage report -m
coverage html
```

## 4. How to launch the celery workers
Since Celery 4.0, the workers only work on linux, to launch them use the following commands:
```sh
################## In Debug mode ##################

# launch Worker
celery worker -A application -l debug --events

# launch heartbeat
celery beat -A application --loglevel=debug --detach

# launch camera 
celery events -A application --loglevel=debug --camera=django_celery_monitor.camera.Camera --frequency=2.0 --detach

################## In Production mode ##################

# launch Worker
celery worker -A application -l info --events

# launch heartbeat
celery beat -A application --loglevel=info --detach

# launch camera 
celery events -A application --loglevel=info --camera=django_celery_monitor.camera.Camera --frequency=2.0 --detach
```

## 5. How to setup Travis for continuous integration.

You will need to set environment variables as followed:

The travis deploy script is set to create a release on github whenever a new tag is pushed. Thus, you need to create a github **token** and set it in travis in an **encrypted** fashion.

When a build is successful, Travis push on production/development environment which runs on CloudFoundry hosted by IBM Bluemix.
This is controlled by the branch being updated. Please confer to Bluemix documentation to gather the correct settings. They can also easily be changed for any cloudfoundry-based hosting service (e.g. Heroku).

**Non encrypted environment vars that need to be set:**

| Key                      | Value                                            |
|--------------------------|--------------------------------------------------|
| ARTIFACT_NAME            | 'release_filename.zip'                           |
| BLUEMIX_USERNAME         | 'firstname.lastname@host.com'                    |
| BLUEMIX_API_GATEWAY      | 'https://api.eu-gb.bluemix.net'                  | 
| BLUEMIX_API_ORGANISATION | 'MyFantasticOrganisation'                        |
| BLUEMIX_API_SPACE        | 'MyEnvironment'                                  |

**Encrypted environment vars that need to be set:**

| Key                      | Value                                            |
|--------------------------|--------------------------------------------------|
| SECRET_KEY               | '##############################################' |
| AWS_USER                 | '##############################################' |
| AWS_SECRET_KEY           | '##############################################' |
| FIELD_ENCRYPTION_KEY     | '##############################################' |
| BluemixPassword          | '##############################################' |
| GITHUB_OAUTH_TOKEN       | '##############################################' |

**There are also other environment variables, however they do not require to be changed:**

| Key                      | Value                                            |
|--------------------------|--------------------------------------------------|
| RABBITMQ_URL             | 'amqp://guest:guest@localhost:5672/'             |
| DATABASE_URL             | 'postgres://postgres:@localhost:5432/travisci'   |
| DEBUG                    | 'True'                                           |
| TRAVIS                   | 'True'                                           |
| EMAIL_DEFAULT_SENDER     | 'local@local.host'                               |
