from django.urls import path
from . import views

# creating custom urls for the API
# Design an API to access the data stored in the database.
# Create an endpoint to trigger the scraper for today.

urlpatterns = [
    path('scraped-data/', views.ScrapedDataList.as_view(),
         name='scraped-data-list'),
    path('trigger-scraper/', views.TriggerScraper.as_view(), name='trigger-scraper'),
]
