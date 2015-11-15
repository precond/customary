# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiToken',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('token', models.CharField(max_length=128)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='ApiUser',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('comment', models.TextField(max_length=1024)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='apitoken',
            name='api_user',
            field=models.ForeignKey(to='api.ApiUser'),
        ),
    ]
