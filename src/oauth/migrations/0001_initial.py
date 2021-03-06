# Generated by Django 3.2.8 on 2021-11-05 02:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import src.oauth.uploading
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=150, unique=True, verbose_name='Е-маил')),
                ('password', models.CharField(blank=True, max_length=18, null=True, verbose_name='Пароль')),
                ('join_date', models.DateTimeField(auto_now_add=True)),
                ('country', models.CharField(blank=True, max_length=30, null=True, verbose_name='Страна')),
                ('city', models.CharField(blank=True, max_length=30, null=True, verbose_name='Город')),
                ('bio', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Биография')),
                ('display_name', models.CharField(blank=True, help_text='Может быть любым, поумолчанию это имя вашей почты (Все что идет до @).', max_length=30, null=True, verbose_name='Показываемое имя')),
                ('is_authenticated', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(default='2021-11-05 02:48', editable=False, verbose_name='Дата и время создания')),
            ],
            options={
                'verbose_name': 'Авторизованный пользователь',
                'verbose_name_plural': 'Авторизованные пользователи',
            },
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(default='2021-11-05 02:48', editable=False, verbose_name='Дата и время создания')),
                ('deleted', models.BooleanField(default=False)),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='oauth.auth')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='oauth.auth')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), src.oauth.uploading.validate_size_image])),
                ('create_date', models.DateField(default='2021-11-05 02:48', editable=False, verbose_name='Дата и время создания')),
                ('deleted', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='avatar', to='oauth.auth')),
            ],
            options={
                'verbose_name': 'Аватар пользователя',
                'verbose_name_plural': 'Автары пользователей',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=50, unique=True)),
                ('last_name', models.CharField(max_length=50, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('age', models.PositiveIntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'db_table': 'user',
            },
        ),
    ]
