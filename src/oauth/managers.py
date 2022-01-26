from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from django.db.models.manager import Manager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a Users with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class AuthManager(Manager):

    def create(self, *args, **kwargs):
        if kwargs.get('email'):
            if kwargs.get('is_authenticated'):
                return super().create(*args, **kwargs)
            elif kwargs.get('password'):
                return super().create(*args, *kwargs)
            raise ValueError("При регистрации нужно без использования стонних сервисов пароль обязателен")
        raise ValueError("E-mail обязателен при регистрации")

    def save(self, is_authenticated: bool, *args, **kwargs):
        if self.is_authenticated:
            return 123
        data = kwargs
        return f'{kwargs}'
