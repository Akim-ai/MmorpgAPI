# Generated by Django 3.2.8 on 2021-11-05 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auth',
            name='create_date',
            field=models.DateTimeField(default='2021-11-05 02:49', editable=False, verbose_name='Дата и время создания'),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='create_date',
            field=models.DateField(default='2021-11-05 02:49', editable=False, verbose_name='Дата и время создания'),
        ),
        migrations.AlterField(
            model_name='follower',
            name='create_date',
            field=models.DateTimeField(default='2021-11-05 02:49', editable=False, verbose_name='Дата и время создания'),
        ),
    ]