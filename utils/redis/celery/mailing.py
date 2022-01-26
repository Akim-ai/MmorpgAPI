import asyncio

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


async def a_send_mass_different_email(
        subject: str, recipient_list: str, message: str = f'Check profile',
        from_email: str = settings.EMAIL_HOST_USER_FULL
):
    a_send_mail = sync_to_async(send_mail)
    await a_send_mail(
        subject=f'{subject}',
        message=f'{message}',
        recipient_list=[recipient_list],
        from_email=from_email,
    )
    return


def a_run_mass_send_mail(prepare_mail):
    async def runner(data:  dict, *args, **kwargs) -> bool:
        if not data:
            return False
        task_list = []
        for i in data.keys():
            task = asyncio.create_task(
                prepare_mail(data=data[i], key=i)
            )
            task_list.append(task)
        await asyncio.gather(*task_list)
        return True
    return runner
