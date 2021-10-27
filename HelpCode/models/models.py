from datetime import datetime

from django.db import models

from .managers import DefaultManager


class DefaultModel(models.Model):
    deleted = models.BooleanField('Удалить', default=False)
    create_date = models.DateField(
        "Дата создания", default=datetime.utcnow().date().strftime("%Y-%m-%d"),
        editable=True
    )
    objects = DefaultManager()

    def save(self, *args, **kwargs):
        model = type(self)
        super(model, self).save(*args, **kwargs)
