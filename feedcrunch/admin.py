"""Admin module for Django."""
from django.contrib import admin

import re, uuid, datetime

from .models import *

admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(RSSFeed_Sub)
admin.site.register(RSSArticle_Assoc)

# ==================== FEEDUSER ============================
class FeedUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined', 'country', 'is_staff', '_get_post_count', '_get_rss_subscribtion_count')
    ordering = ('-date_joined',)

    def _get_post_count(self, obj):
        return obj.get_post_count()
    _get_post_count.short_description = "Post Count"

    def _get_rss_subscribtion_count(self, obj):
        return obj.get_rss_subscribtion_count()
    _get_rss_subscribtion_count.short_description = "RSS Count"
    #_get_post_count.admin_order_field = 'get_post_count'

    """
    def has_add_permission(self, request, obj=None):
        ''' Forbid adding via admin interface '''
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    """

    search_fields = ('username', 'country', 'email')
    list_filter = ('country',)

admin.site.register(FeedUser, FeedUserAdmin)

# ==================== Option ============================
class OptionAdmin(admin.ModelAdmin):
    list_display = ('parameter', 'value')
    ordering = ('parameter',)

    search_fields = ('parameter',)

admin.site.register(Option, OptionAdmin)


# ==================== Tag ============================
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', '_get_post_count')
    ordering = ('name',)

    def _get_post_count(self, obj):
        return obj.get_post_count()
    _get_post_count.short_description="Post Count"

    search_fields = ('name',)

admin.site.register(Tag, TagAdmin)


# ==================== Post ============================
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'get_domain', 'clicks', '_get_tags_count')
    ordering = ('-id',)

    def _get_tags_count(self, obj):
        return obj.get_tags_count()
    _get_tags_count.short_description="Tag Count"

    search_fields = ('user', 'title', 'get_domain')
    list_filter = ('user',)

admin.site.register(Post, PostAdmin)

# ==================== RSS Feed ============================
class RSSFeedAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_domain', 'link', '_get_articles_count')
    ordering = ('-id',)

    def _get_articles_count(self, obj):
        return obj.count_articles()
    _get_articles_count.short_description="Articles Count"

    search_fields = ('title', 'get_domain')

admin.site.register(RSSFeed, RSSFeedAdmin)

# ==================== RSSArticles =========================
class RSSArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'rssfeed', 'title', 'get_domain', 'link', 'added_date')
    ordering = ('-id',)

    search_fields = ('title', 'get_domain')

admin.site.register(RSSArticle, RSSArticlesAdmin)

# ==================== Estimator ============================
class EstimatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'creation_date', 'last_modified_date', 'description')
    ordering = ('-last_modified_date',)

    search_fields = ('description',)

admin.site.register(Estimator, EstimatorAdmin)


# ==================== FEEDUSER ============================
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', '_get_rssfeed_count')
    ordering = ('name',)
    exclude = ("guid", )

    def _get_rssfeed_count(self, obj):
        return obj.get_rssfeed_count()
    _get_rssfeed_count.short_description = "RSS Feed Count"

    search_fields = ('name',)

admin.site.register(Interest, InterestAdmin)


#admin.site.register(RSSArticle)
