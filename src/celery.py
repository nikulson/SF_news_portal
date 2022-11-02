from os import environ
from celery import Celery
from django.conf import settings

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
app.autodiscover_tasks()
