from os import environ
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

environ["DJANGO_SETTINGS_MODULE"] = f"src.config.settings"

app = Celery('news_portal')

app.conf.update({
    'broker_url': settings.CELERY['BROKER_URL'],
    'result_backend': settings.CELERY['RESULT_BACKEND_URL'],
    'broker_transport_options': settings.CELERY['BROKER_TRANSPORT_OPT'],
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json']
})

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(
    # lambda: settings.INSTALLED_APPS, force=True
)

app.conf.beat_schedule = {
    'send_email_every_monday_8clock': {
        'task': 'src.news.tasks.send_mail_every_week',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

