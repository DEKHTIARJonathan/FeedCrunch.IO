#!/usr/bin/env python
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
from .model_files.models_rssfeed import *
from .model_files.models_rssarticle import *

admin.site.register(Continent)
admin.site.register(Country)

# ==================== FEEDUSER ============================
class FeedUserAdmin(admin.ModelAdmin):
	list_display = ('username', 'date_joined', 'country', 'is_staff', '_get_post_count')
	ordering = ('-date_joined',)

	def _get_post_count(self, obj):
		return obj.get_post_count()
	_get_post_count.short_description = "Post Count"
	#_get_post_count.admin_order_field = 'get_post_count'


admin.site.register(FeedUser, FeedUserAdmin)


# ==================== Option ============================
class OptionAdmin(admin.ModelAdmin):
	list_display = ('parameter', 'value')
	ordering = ('parameter',)

admin.site.register(Option, OptionAdmin)


# ==================== Tag ============================
class TagAdmin(admin.ModelAdmin):
	list_display = ('name', '_get_post_count')
	ordering = ('name',)

	def _get_post_count(self, obj):
		return obj.get_post_count()
	_get_post_count.short_description="Post Count"

admin.site.register(Tag, TagAdmin)


# ==================== Post ============================
class PostAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'title', 'get_domain', 'clicks', '_get_tags_count')
	ordering = ('-id',)

	def _get_tags_count(self, obj):
		return obj.get_tags_count()
	_get_tags_count.short_description="Tag Count"

admin.site.register(Post, PostAdmin)

# ==================== RSS Feed ============================
class RSSFeedAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'title', 'get_domain', 'link', 'added_date')
	ordering = ('-id',)

admin.site.register(RSSFeed, RSSFeedAdmin)

# ==================== RSSArticles =========================
class RSSArticlesAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'rssfeed', 'title', 'get_domain', 'link', 'added_date')
	ordering = ('-id',)

admin.site.register(RSSArticle, RSSArticlesAdmin)

#admin.site.register(RSSArticle)
