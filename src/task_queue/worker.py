import smtplib

from celery import Celery

from src.config import settings
from src.task_queue.msg_forms import (
    get_forgot_password_message,
    get_reset_password_message,
)

app_celery = Celery(
    'app_celery', broker=settings.CELERY_BROKER, backend=settings.CELERY_BACKEND
)

app_celery.conf.broker_connection_retry_on_startup = True


@app_celery.task(bind=True)
def send_forgot_password_msg(self, email: str, link: str):
    email = get_forgot_password_message(email_to=email, link=link)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)


@app_celery.task(bind=True)
def send_reset_password_msg(self, email: str):
    email = get_reset_password_message(email_to=email)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, timeout=30) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
