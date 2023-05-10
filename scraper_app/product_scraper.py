from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.conf import settings
from .models import Keyword, ScrapedData

# getting the scrap url from settings.py as defined
BASE_URL = settings.AMAZON_SCRAP_BASE_URL


class ScrapProduct:
    # num_items = 5 if not provided
    def __init__(self, num_items=5):
        self.num_items = num_items

    # open the driver
    def open_driver(self):
        self.driver = webdriver.Chrome()  # used chrome driver

    # close the driver
    def close_driver(self):
        self.driver.quit()

    """get_search_results() => Main reason of using this method is to make sure the search works properly.
    we could use the search url directly to fetch data based on keywords for example: https://www.amazon.co.uk/s?k=car+parts
    But in near future if the search url changes, we will have to change the code.
    """

    def get_search_results(self, keyword_instance):
        query = keyword_instance.word
        self.open_driver()
        self.driver.get(BASE_URL)
        # accepting cookies (Not required but good to have)
        self.accept_cookie()
        # find element by id of search input box
        search_box = self.driver.find_element(By.ID, 'twotabsearchtextbox')
        # sending the query to search box
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        # time.sleep(5)

        try:
            # waiting for the search results to load
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".s-result-item.s-asin")))
            # getting the search results elements by using css Selector, Could use Xpath but css selector is easier to undertsnad
            result_elements = self.driver.find_elements(
                By.CSS_SELECTOR, ".s-result-item.s-asin")
            # passing the result elements to get_product_details() method to get the product details
            items = self.get_product_details(result_elements, keyword_instance)
        except Exception as e:
            print("Error: ", e)
            self.close_browser()
            items = []

        self.close_browser()
        self.close_driver()
        return items

    # getting the product details based on keywords and storing data in database
    def get_product_details(self, products, keyword):
        # items is a list of dictionaries
        items = []
        # count is used to limit the number of items to be scraped
        count = 0

        for product in products:
            try:
                if count >= self.num_items:  # Break the loop when the counter reaches the limit
                    break
                # waiting for the product title to load for title_element
                title_element = WebDriverWait(product, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'h2 a.a-link-normal')))
                title = title_element.text
                # checking if title exists
                if not title:
                    continue
                # getting the link of the product
                link = title_element.get_attribute('href')

                # checking if results is organic or sponsored
                sponsored = 'AdHolder' in product.get_attribute(
                    'class').split()
                # getting price of the product with fraction number
                price_whole_element = product.find_element(
                    By.CSS_SELECTOR, '.a-price .a-price-whole')
                price_fraction_element = product.find_element(
                    By.CSS_SELECTOR, '.a-price .a-price-fraction')
                price = f'{price_whole_element.text}.{price_fraction_element.text}'
                # print(price)

                # getting the rating of the product from area-label attribute
                rating_element = product.find_element(
                    By.XPATH, './/span[contains(@aria-label, "out of 5 stars")]')
                rating = rating_element.get_attribute('aria-label')
                # print(rating)

                """Open the product page in a new tab (so the main loop don't breaks)
                and get the description. This is for the description of the product.
                This was necessery to fetch description as on search results product description not available.
                """
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.driver.get(link)

                description_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#feature-bullets ul.a-unordered-list')))
                description = description_element.get_attribute('innerHTML')

                # Close the product page tab and switch back to the search results tab
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])

                # Create a dictionary of the product details
                item = {
                    'title': title, 'link': link, 'sponsored': sponsored,
                    'price': price, 'description': description, 'rating': rating
                }
                # Append the dictionary to the items list
                items.append(item)

                # Save the data to the database as per our model schema
                product_instance = ScrapedData(
                    title=title, link=link, sponsored=sponsored,
                    price=price, description=description, rating=rating,
                    keyword=keyword
                )
                product_instance.save()
                # Increment the counter
                count += 1

            except Exception as e:
                # getting error if any
                print("Error in getting product details: ", e)
                continue

        return items

    # Accept the cookie
    def accept_cookie(self):
        cookie_btn = self.driver.find_element(
            By.CSS_SELECTOR, 'input#sp-cc-accept')
        time.sleep(5)
        cookie_btn.click()

    # Close the browser
    def close_browser(self):
        return self.driver.quit()


def run_scraper():
    # Fetch the keywords from the database
    keyword_instances = Keyword.objects.all()
    # number of items to scrape per keyword
    num_items_to_fetch = 1
    # Initialize the scraper
    scraper = ScrapProduct(num_items_to_fetch)

    # Loop through the keyword instances and scrape data for each keyword in the database
    # (Accept a list of keywords as input, e.g. cat food, dog food, car parts, gym clothes men.)
    for keyword_instance in keyword_instances:
        print(f"Scraping for keyword: {keyword_instance.word}")
        items = scraper.get_search_results(keyword_instance)
        # Print the number of items scraped for each keyword (in terminal to check)
        print(
            f"Scraped {len(items)} items for keyword: {keyword_instance.word}")
