from smtplib import SMTP_SSL
from .worker import celery_app
from .email_templates import reminder_email_template
from app.config import settings

@celery_app.task
def send_due_reminder(title:str, email:str, due_date: str):
    msg = reminder_email_template(title, email, due_date)
    msg["From"] = settings.SMTP_USER

    try:
        with SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg)
        print(f"Reminder sent to {email} for task {title}")
    except Exception as e:
        print(f"Failed to sent reminder: {e}")