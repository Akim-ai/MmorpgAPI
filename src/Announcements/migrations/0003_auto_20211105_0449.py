# Generated by Django 3.2.8 on 2021-11-05 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='create_date',
            field=models.DateTimeField(default='2021-11-05 02:49', editable=False, verbose_name='Дата и время создания'),
        ),
        migrations.AlterField(
            model_name='announcementpicture',
            name='create_date',
            field=models.DateTimeField(default='2021-11-05 02:49', editable=False, verbose_name='Дата и время создания'),
        ),
        migrations.AlterField(
            model_name='announcementresponse',
            name='create_date',
            field=models.DateTimeField(default='2021-11-05 02:49', editable=False, verbose_name='Дата и время создания'),
        ),
    ]
