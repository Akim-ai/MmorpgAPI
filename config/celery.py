import os
from time import sleep

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'mass_email_confirm': {
        'task': 'src.oauth.tasks.periodic_send_mass_confirm_email',
        'schedule': 15.0*4,
    },
    'mass_response_create': {
        'task': 'src.Announcements.tasks.periodic_send_mass_response_mail',
        'schedule': 15.0*60,
    },
    'mass_response_accept': {
        'task': 'src.Announcements.tasks.periodic_send_mass_response_accept_mail',
        'schedule': 15.0*60,
    }
}
