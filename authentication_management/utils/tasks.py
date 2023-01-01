import os

from celery import Celery
from pydantic import EmailStr

from authentication_management.utils.email import EmailGenerator

celery_app: Celery = Celery(
    "email-worker",
    backend=os.getenv("REDIS_HOST"),
    broker=os.getenv("AMQP_URL"),
)
celery_app.conf.task_routes = {
    "authentication_management.utils.tasks.send_account_verify_email": "send_verify_email",
    "authentication_management.utils.tasks.send_account_reset_password_email": "send_change_password_email"}

celery: Celery = celery_app


@celery_app.task(acks_late=True)
def send_account_verify_email(email: EmailStr, token: str) -> None:
    email_handler: EmailGenerator = EmailGenerator()
    email_handler.get_account_verify_email(to_email=email,
                                           url=str(os.getenv("FRONT_END_URL")) + "?user_verify=" + token)


@celery_app.task(acks_late=True)
def send_account_reset_password_email(email: EmailStr, token: str) -> None:
    email_handler = EmailGenerator()
    email_handler.get_account_change_password_email(to_email=email,
                                                    url=str(os.getenv(
                                                        "FRONT_END_URL")) + "?reset_password=" + token)
