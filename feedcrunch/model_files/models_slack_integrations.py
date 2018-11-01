#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from feedcrunch.model_files.models_user import FeedUser

from encrypted_model_fields.fields import EncryptedCharField


############################## TAG MODEL ###################################

class SlackIntegration(models.Model):
    id           = models.AutoField(primary_key=True)
    user         = models.ForeignKey(FeedUser, related_name='rel_slack_integrations', on_delete=models.CASCADE)
    team_name    = models.CharField(max_length=100, blank=False, null=False)
    channels     = models.CharField(max_length=100, blank=True, null=True, default="")
    access_token = EncryptedCharField(max_length=500, blank=False, null=False)

    class Meta:
        unique_together = (("team_name", "user"),)

    def __str__(self):
        return self.team_name + " // " + self.user.username
