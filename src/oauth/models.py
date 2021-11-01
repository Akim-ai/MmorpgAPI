from datetime import datetime

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db.models import Manager

from .managers import CustomUserManager

import uuid
from django.core.validators import FileExtensionValidator

from .uploading import validate_size_image

from utils.managers import DefaultManager, DeletedManager


class User(AbstractUser):
    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    first_name = models.CharField(max_length=50, unique=True)
    last_name = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        if self.first_name:
            if self.last_name:
                return f'{self.first_name} {self.last_name}'
            return f'{self.first_name}'
        if self.last_name:
            return f'{self.last_name}'
        return f'{self.email}'

    class Meta:
        db_table = "user"
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"


class Auth(models.Model):
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=2000, blank=True, null=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.show_display_name

    class Meta:
        verbose_name = 'Авторизованный пользователь'
        verbose_name_plural = 'Авторизованные пользователи'

    @property
    def is_authenticated(self):
        """Способ узнать был ли пользователь аутентифитирован"""
        return True

    @property
    def show_display_name(self):
        if self.display_name:
            return f'{self.display_name}'
        name = self.email.split('@')[0]
        return f'{name}'


class Avatar(models.Model):
    user = models.ForeignKey(Auth, on_delete=models.PROTECT, related_name='avatar')
    img = models.ImageField(
        upload_to='', blank=True,
        null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg']),
                               validate_size_image]
    )
    create_date = models.DateField(
        "Дата создания", default=datetime.utcnow().date().strftime("%Y-%m-%d"),
        editable=True
    )
    deleted = models.BooleanField(default=False)

    objects = DefaultManager()
    objects_del = DeletedManager()
    objects_all = Manager()

    def __str__(self):
        return f'{self.img}'

    class Meta:
        verbose_name = 'Аватар пользователя'
        verbose_name_plural = 'Автары пользователей'

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
        return self


class Follower(models.Model):
    user = models.ForeignKey(Auth, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(Auth, on_delete=models.CASCADE, related_name='subscribers')
    create_date = models.DateField(
        "Дата создания", default=datetime.utcnow().date().strftime("%Y-%m-%d"),
        editable=True
    )
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.subscriber} подписан на {self.user}'

    objects = DefaultManager()
    objects_del = DeletedManager()
    objects_all = Manager()

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
        return self

