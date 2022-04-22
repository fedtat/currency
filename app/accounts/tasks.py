from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


@shared_task
def debug():
    from time import sleep
    sleep(10)
    # print('Hello From Celery Task')


@shared_task
def send_activation_email(username: str, email: str):
    subject = 'Sign Up'
    body = f'''
        Activation Link:
        {settings.HTTP_SCHEMA}://{settings.DOMAIN}{reverse('accounts:activate-user', args=[username])}
        '''
    email_from = settings.DEFAULT_FROM_EMAIL
    send_mail(
        subject,
        body,
        email_from,
        [email],
        fail_silently=False
    )
