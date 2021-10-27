# Generated by Django 3.2.8 on 2021-10-26 22:56

from django.db import migrations, models
import django.db.models.deletion
import src.Announcements.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('HelpCode', '0001_initial'),
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('defaultmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='HelpCode.defaultmodel')),
                ('title', models.CharField(max_length=150, verbose_name='Заголовок')),
                ('description', models.TextField(max_length=1500, verbose_name='Описание')),
                ('category', models.CharField(choices=[('Та', 'Танк'), ('Хи', 'Хил'), ('ДД', 'Демедж-Диллер'), ('То', 'Торговец'), ('ГМ', 'Гилдмастер'), ('Кв', 'Квестгивер'), ('Ку', 'Кузнец'), ('Ко', 'Кожевник'), ('Зе', 'Зельевар'), ('МЗ', 'Мастер заклинаний')], max_length=2, verbose_name='Категория')),
                ('user', models.ForeignKey(help_text='Пользователь', on_delete=django.db.models.deletion.CASCADE, to='oauth.auth', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Объявление',
                'verbose_name_plural': 'Объявления',
            },
            bases=('HelpCode.defaultmodel',),
        ),
        migrations.CreateModel(
            name='AnnouncementResponse',
            fields=[
                ('defaultmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='HelpCode.defaultmodel')),
                ('text', models.TextField(max_length=1000, verbose_name='Сообщение')),
                ('accepted', models.BooleanField(default=False, verbose_name='Одобрен')),
                ('announcement_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='announcements.announcement', verbose_name='Относится к объявлению')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oauth.auth')),
            ],
            options={
                'verbose_name': 'Отклик',
                'verbose_name_plural': 'Отклики',
                'ordering': ['-accepted'],
            },
            bases=('HelpCode.defaultmodel',),
        ),
        migrations.CreateModel(
            name='AnnouncementPicture',
            fields=[
                ('defaultmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='HelpCode.defaultmodel')),
                ('img', models.ImageField(max_length=255, upload_to=src.Announcements.models.announcement_picture_directory_path, verbose_name='Изображение')),
                ('announcement_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='announcements.announcement', verbose_name='Относится к объявлению')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oauth.auth', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
            bases=('HelpCode.defaultmodel',),
        ),
    ]