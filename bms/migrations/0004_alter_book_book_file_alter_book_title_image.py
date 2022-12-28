# Generated by Django 4.1.4 on 2022-12-27 06:33

import bms.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bms', '0003_book_date_of_book_book_identifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_file',
            field=models.FileField(blank=True, null=True, upload_to=bms.models.book_dir),
        ),
        migrations.AlterField(
            model_name='book',
            name='title_image',
            field=models.ImageField(blank=True, null=True, upload_to=bms.models.book_cover_dir),
        ),
    ]
