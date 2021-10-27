from django.db import models

import datetime

from src.oauth.models import Auth as User
from HelpCode.models.models import DefaultModel


class Announcement(DefaultModel):
    """Объявление"""
    user = models.ForeignKey(User, help_text='Пользователь',
                             on_delete=models.CASCADE,
                             verbose_name="Пользователь")
    title = models.CharField('Заголовок', max_length=150)
    description = models.TextField('Описание', max_length=1500)
    category_choices = (
        ('Та', 'Танк'),
        ("Хи", "Хил"),
        ("ДД", "Демедж-Диллер"),
        ("То", "Торговец"),
        ("ГМ", "Гилдмастер"),
        ("Кв", "Квестгивер"),
        ("Ку", "Кузнец"),
        ("Ко", "Кожевник"),
        ("Зе", "Зельевар"),
        ("МЗ", "Мастер заклинаний")
    )
    category = models.CharField("Категория", max_length=2, choices=category_choices)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


def announcement_picture_directory_path(instance, filename):
    date = datetime.date.today()
    return 'users/{0}/AnnouncementPicture/{1}/{2}/{3}/{4}'.format(instance.user.id, date.year,
                                                                  date.month, date.day, filename)


class AnnouncementPicture(DefaultModel):
    """Картинки для объявлений"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    img = models.ImageField(
        'Изображение',
        upload_to=announcement_picture_directory_path,
        max_length=255
    )
    announcement_id = models.ForeignKey(
        Announcement, on_delete=models.CASCADE,
        verbose_name="Относится к объявлению",
        related_name='pictures'
    )

    def __str__(self):
        return f'{self.img}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class AnnouncementResponse(DefaultModel):
    """Отклики на объявления"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Сообщение', max_length=1000)
    accepted = models.BooleanField('Одобрен', default=False)
    announcement_id = models.ForeignKey(
        Announcement, on_delete=models.CASCADE,
        verbose_name='Относится к объявлению',
        related_name='responses',
    )

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-accepted']
