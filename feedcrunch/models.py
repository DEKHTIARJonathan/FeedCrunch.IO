# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib import admin

import re, uuid, datetime

from .model_files.models_geo import *
from .model_files.models_user import *
from .model_files.models_tag import *
from .model_files.models_post import *
from .model_files.models_options import *

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(FeedUser)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Option)
