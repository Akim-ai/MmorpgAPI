from django.db import models

from datetime import datetime

from src.oauth.models import Auth as User
from utils.managers import DefaultManager, DeletedManager
from django.db.models import Manager


category_choices = (
    ('Та', 'Танк'),
    ("Хи", "Хил"),
    ("ДД", "Демедж Диллер"),
    ("То", "Торговец"),
    ("ГМ", "Гилдмастер"),
    ("Кв", "Квестгивер"),
    ("Ку", "Кузнец"),
    ("Ко", "Кожевник"),
    ("Зе", "Зельевар"),
    ("МЗ", "Мастер Заклинаний")
)


class Announcement(models.Model):
    """Объявление"""
    user = models.ForeignKey(
        User, help_text='Пользователь',
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    title = models.CharField('Заголовок', max_length=150)
    description = models.TextField('Описание', max_length=1500)
    category = models.CharField(
        "Категория", max_length=2,
        choices=category_choices
    )
    create_date = models.DateTimeField(
        "Дата и время создания", auto_now_add=True,
        editable=False
    )
    deleted = models.BooleanField(default=False)

    objects = DefaultManager()
    objects_del = DeletedManager()
    objects_all = Manager()

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ('-create_date', )

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
        return self


def announcement_picture_directory_path(instance, filename):
    date = datetime.today().date()
    return 'users/{0}/Announcement/{1}/Pictures/{2}/{3}/{4}/{5}'.format(
        instance.user, instance.announcement,
        date.year, date.month, date.day,
        filename
    )


class AnnouncementPicture(models.Model):
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
    announcement = models.ForeignKey(
        Announcement, on_delete=models.CASCADE,
        verbose_name="Относится к объявлению",
        related_name='pictures'
    )
    create_date = models.DateTimeField(
        "Дата и время создания", auto_now_add=True,
        editable=False
    )
    deleted = models.BooleanField(default=False)

    objects = DefaultManager()
    objects_del = DeletedManager()
    objects_all = Manager()

    def __str__(self):
        return f'{self.img}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
        return self


class AnnouncementResponse(models.Model):
    """Отклики на объявления"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Сообщение', max_length=1000)
    accepted = models.BooleanField('Одобрен', null=True)
    announcement = models.ForeignKey(
        Announcement, on_delete=models.CASCADE,
        verbose_name='Относится к объявлению',
        related_name='responses',
    )
    create_date = models.DateTimeField(
        "Дата и время создания", auto_now_add=True,
        editable=False
    )
    deleted = models.BooleanField(default=False)

    objects = DefaultManager()
    objects_del = DeletedManager()
    objects_all = Manager()

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-accepted', '-create_date']

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()
        return self
