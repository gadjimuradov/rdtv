import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','dream.settings.production')

from django.conf import settings

app = Celery('dream')

app.config_from_object('django.conf.settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)