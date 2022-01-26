import asyncio

from celery import shared_task
from django.conf import settings
from django.urls import reverse

from config.celery import app
from utils.redis.backend_managment import set_data_task, get_data_task
from utils.redis.celery.mailing import a_run_mass_send_mail, a_send_mass_different_email


@app.task
def send_response_create_mail(email: str):
    return prepare_send_response_create_email(email=email)

@set_data_task
def prepare_send_response_create_email(email: str, data: dict = {}, *args, **kwargs):
    new_data = {email: {
        'response_cnt': data.get(email, {}).get('response_cnt', 0) + 1
    }}
    return new_data, email

@shared_task
def periodic_send_mass_response_mail(*args, **kwargs):
    return periodic_send_response_create_email(*args, **kwargs)

@get_data_task
def periodic_send_response_create_email(data, *args, **kwargs) -> bool:
    success = asyncio.run(a_prepare_mass_response_create(data, *args, **kwargs))
    return success

@a_run_mass_send_mail
async def a_prepare_mass_response_create(data, key, *args, **kwargs):
    task = asyncio.create_task(
        a_send_mass_different_email(
            subject=f'You got {data.get("response_cnt")} new {"response to your announcement." if data["response_cnt"] < 2 else "responses to yours announcements."}',
            message=f'To see a new response check the link: \n{settings.INDEX_URL+reverse("my-profile")}',
            recipient_list=key
        )
    )
    return task



@app.task
def send_response_accept_mail(email: str):
    return prepare_send_response_accept_email(email)

@set_data_task
def prepare_send_response_accept_email(email: str, data: dict = {}, *args, **kwargs):
    new_data = {email: {
        'accepted_response_cnt': data.get(email, {}).get('accepted_response_cnt', 0) + 1
    }}
    return new_data, email

@shared_task
def periodic_send_mass_response_accept_mail(*args, **kwargs):
    return periodic_send_response_accept_email(*args, **kwargs)

@get_data_task
def periodic_send_response_accept_email(data, *args, **kwargs) -> bool:
    success = asyncio.run(a_prepare_mass_response_accept(data, *args, **kwargs))
    return success

@a_run_mass_send_mail
async def a_prepare_mass_response_accept(data, key, *args, **kwargs):
    task = asyncio.create_task(
        a_send_mass_different_email(
            subject=f'You got {data.get("accepted_response_cnt")} new accepted {"response" if data["accepted_response_cnt"] < 2 else "responses"}.',
            message=f'To see a accepted responses check the link: \n{settings.INDEX_URL+reverse("my-profile")}',
            recipient_list=key
        )
    )
    return task