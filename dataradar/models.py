from __future__ import unicode_literals
from django.db import models

import re

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    link = models.URLField(max_length=2000)
    when = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField()
    activeLink = models.BooleanField()

    def get_date(self):
        return self.when.strftime("%Y/%m/%d %H:%M")

    def get_domain(self):
        starts = [match.start() for match in re.finditer(re.escape("/"), self.link)]
        if len(starts) > 2:
            return self.link[starts[1]+1:starts[2]]
        elif len(starts) == 2:
            return self.link[starts[1]+1:]
        else:
            return str("error")
