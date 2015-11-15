# coding=utf-8


from django.contrib.auth.models import User
from django.db import models


class ApiUser(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    comment = models.TextField(max_length=1024)

    class Meta:
        app_label = 'api'


class ApiToken(models.Model):
    api_user = models.ForeignKey(ApiUser)
    token = models.CharField(max_length=128)
    last_seen = models.DateTimeField(auto_now=True)
    comment = models.TextField(max_length=1024)

    class Meta:
        app_label = 'api'
