# Generated by Django 3.2.8 on 2021-11-05 03:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0003_auto_20211105_0503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auth',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 5, 7, 21, 485721), editable=False, verbose_name='Дата и время создания'),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='create_date',
            field=models.DateField(default='2021-11-05 05:07', editable=False, verbose_name='Дата и время создания'),
        ),
        migrations.AlterField(
            model_name='follower',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 5, 5, 7, 21, 486719), editable=False, verbose_name='Дата и время создания'),
        ),
    ]
