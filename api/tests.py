import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from scraper_app.models import Keyword, ScrapedData


class ScrapedDataListTests(APITestCase):
    def setUp(self):
        # created test data for the API
        self.keyword = Keyword.objects.create(word='laptop')
        self.date_scraped = datetime.datetime.now()
        self.scraped_data = ScrapedData.objects.create(
            title='Test Laptop',
            link='https://example.com/test-laptop',
            sponsored=False,
            price='1200.00',
            description='Test laptop description',
            rating='4.5 out of 5 stars',
            keyword=self.keyword,
            date_scraped=self.date_scraped,
        )
        self.url = reverse('scraped-data-list')

    def test_get_scraped_data_list(self):
        # teesting if the API returns a list of scraped data
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_scraped_data_list_filtered(self):
        # Testing if the API returns the correct filtered data based on the provided keyword and date
        response = self.client.get(
            self.url, {'keyword': 'laptop', 'date': self.date_scraped.date()})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TriggerScraperTests(APITestCase):
    def test_trigger_scraper(self):
        # Testing if the scraper is triggered when the endpoint is accessed
        url = reverse('trigger-scraper')
        with patch('api.views.run_scraper') as mock_run_scraper:
            response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'status': 'Scraper started successfully.'})
        self.assertTrue(mock_run_scraper.called)
