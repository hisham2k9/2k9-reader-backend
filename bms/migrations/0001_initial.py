# Generated by Django 4.1.4 on 2022-12-24 14:15

import bms.models
import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('author', models.CharField(blank=True, max_length=200, null=True)),
                ('title_image', models.ImageField(blank=True, null=True, upload_to='uploads/book-covers/')),
                ('language', models.CharField(blank=True, max_length=100, null=True)),
                ('datetime_update', models.DateTimeField(default=datetime.datetime.now)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('owner', models.ForeignKey(blank=True, default=None, null=True, on_delete=models.SET(bms.models.get_sentinel_user), to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
    ]
