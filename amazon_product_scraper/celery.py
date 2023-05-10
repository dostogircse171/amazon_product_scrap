from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta

# setting up the default environment variable for the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'amazon_product_scraper.settings')

# created a new instance of the Celery app with a name 'amazon_product_scraper'
app = Celery('amazon_product_scraper')

# configuring the Celery app using the Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# all tasks in the installed Django apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# scheduled for the Celery app to trigger the scraper task every 24 hours (can be tested by reducing time)
app.conf.beat_schedule = {
    'trigger-scraper-every-24-hours': {
        'task': 'scraper_app.tasks.trigger_scraper',
        'schedule': timedelta(hours=24),
    },
}

# this is for test run the scadule every 1 minutes
# app.conf.beat_schedule = {
#     'trigger-scraper-every-minute': {
#         'task': 'scraper_app.tasks.trigger_scraper',
#         'schedule': timedelta(minutes=1),
#     },
# }
