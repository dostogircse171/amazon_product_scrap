from celery import shared_task
import requests
from django.conf import settings
# we have an api endpoint to run the scraper so we triggered that endpoint.


url = getattr(settings, 'SCRAPER_API_ENDPOINT',
              'http://127.0.0.1:8000/api/trigger-scraper/')


@shared_task
def trigger_scraper():
    response = requests.get(url)
    return response.status_code
