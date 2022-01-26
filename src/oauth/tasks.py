import asyncio

from celery import shared_task
from django.conf import settings

from config.celery import app
from utils.redis.backend_managment import set_data_task, get_data_task
from utils.redis.celery.mailing import a_send_mass_different_email, a_run_mass_send_mail


@app.task
def send_confirm_email(user_email: str, token: str) -> bool:
    return prepare_send_confirm_email(user_email, token)


@set_data_task
def prepare_send_confirm_email(user_email, token, *args, **kwargs):
    data = {user_email: {
        'message': f'{settings.EMAIL_CONFORMATION_URL+ token}/',
    }}
    return data, user_email


@shared_task
def periodic_send_mass_confirm_email(*args, **kwargs) -> bool:
    return periodic_send_confirm_email(*args, **kwargs)


@get_data_task
def periodic_send_confirm_email(data, *args, **kwargs):
    success = asyncio.run(a_prepare_mass_email_confirm(data, *args, **kwargs))
    return success


@a_run_mass_send_mail
async def a_prepare_mass_email_confirm(data, key, *args, **kwargs):
    task = asyncio.create_task(
        a_send_mass_different_email(
            subject='Email conformation.', message=data['message'], recipient_list=key
        )
    )
    return task



