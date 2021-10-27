import datetime
from django.core.exceptions import ValidationError

from config.settings import MAX_MEGABYTE_USER_AVATAR


def get_path_upload_avatar(instance, file) -> str:
    date = datetime.date.today()
    return f'avatar/{instance.id}/{date.year}/{date.month}/{date.day}/{file}'


def validate_size_image(file_obj):
    """ File size check"""
    if file_obj.size > MAX_MEGABYTE_USER_AVATAR * 1024**2:
        raise ValidationError(f"Максимальный размер файла {MAX_MEGABYTE_USER_AVATAR}MB")