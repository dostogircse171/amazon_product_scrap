import datetime
from django.test import TestCase
from unittest.mock import MagicMock, patch
from .models import Keyword, ScrapedData
from .product_scraper import ScrapProduct


class DatabaseSchemaTests(TestCase):
    def test_create_and_retrieve_keyword(self):
        # test the creation and retrieval of a keyword object
        keyword = Keyword.objects.create(word='laptop')
        retrieved_keyword = Keyword.objects.get(pk=keyword.pk)
        self.assertEqual(retrieved_keyword.word, 'laptop')

    def test_create_and_retrieve_scraped_data(self):
        # test the creation and retrieval of a scraped data object
        keyword = Keyword.objects.create(word='laptop')
        date_scraped = datetime.datetime.now()
        scraped_data = ScrapedData.objects.create(
            title='Test Laptop',
            link='https://example.com/test-laptop',
            sponsored=False,
            price='1200.00',
            description='Test laptop description',
            rating='4.5 out of 5 stars',
            keyword=keyword,
            date_scraped=date_scraped,
        )
        retrieved_scraped_data = ScrapedData.objects.get(pk=scraped_data.pk)
        self.assertEqual(retrieved_scraped_data.title, 'Test Laptop')


class ScraperTests(TestCase):
    def setUp(self):
        # create a scraper instance for testing
        self.scraper = ScrapProduct()
        self.scraper.driver = MagicMock()

    @patch('scraper_app.product_scraper.webdriver.Chrome')
    def test_open_driver(self, mock_chrome):
        # test if the webdriver is opened correctly
        self.scraper.open_driver()
        self.assertTrue(mock_chrome.called)

    def test_close_driver(self):
        # test if the webdriver is closed correctly
        self.scraper.driver.quit = MagicMock()
        self.scraper.close_driver()
        self.assertTrue(self.scraper.driver.quit.called)

    def test_accept_cookie(self):
        # test if the accept cookie function works as expected
        self.scraper.driver.find_element.return_value = MagicMock()
        self.scraper.accept_cookie()
        self.assertTrue(self.scraper.driver.find_element.called)
