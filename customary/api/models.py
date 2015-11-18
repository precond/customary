# coding=utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class ApiUser(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    comment = models.TextField(max_length=1024)

    def __str__(self):
        if self.user:
            return '{0} ({1})'.format(self.user, self.comment[:40])
        return self.comment[:40]

    class Meta:
        app_label = 'api'


@python_2_unicode_compatible
class ApiToken(models.Model):
    api_user = models.ForeignKey(ApiUser)
    token = models.CharField(max_length=128)
    last_seen = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=1024)

    def __str__(self):
        if self.api_user.user:
            return '{0} ({1})'.format(self.api_user.user, self.comment[:40])
        return '{0} ({1})'.format(self.api_user, self.comment[:40])

    class Meta:
        app_label = 'api'
