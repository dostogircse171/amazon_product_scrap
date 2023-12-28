# Amazon Product Scraper using Django and Selenium

This project is a Django-based web application that scrapes product data from Amazon's search results using Selenium. It stores the scraped data in an SQLite database and provides an API to access the data and an endpoint to scrap data when hit the endpoint.

## Getting Started

To set up the project locally, follow these steps:

## Installation

1. Clone the repository:

```bash
git clone https://github.com/dostogircse171/amazon_product_scrap.git
```
2. Change into the project directory:

```bash
cd amazon_product_scrap
```
3. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Apply database migrations:

```bash
python manage.py migrate
```
6. Create an admin user(Because we need to add some keywords from admin panel before we can run the scraping):

```bash
python manage.py createsuperuser
```
*Here you will need to provide username,email(optional),password etc...

7. Start the development server:

```bash
python manage.py runserver
```

8. Go to the server admin panel and login as admin:

```bash
http://127.0.0.1:8000/admin
```
8. Go to the server admin panel and login as admin:

```bash
http://127.0.0.1:8000/admin
```
9. Under the Keywords section add as many keywords as you want to scrap the products:

```bash
Eg. Bike, Car Parts, Cat Food, Dog Food etc.
```

10. That's it we are ready to run our scraping.

***The application should now be running at http://127.0.0.1:8000/ (Unless you specified a different port).***

## Run the Scraping using command line
We have created a custom command in django so we can start the scraping manually using django manage.py.
```python
python manage.py run_scraper
```
**This will scrap through all the keywords in the DB one by one **

## Using API Endpoints
We also have API endpoint to fetch all the scraped data and we can filter data based on keywords and date
```python
#Endpoint to fetch all data
http://127.0.0.1:8000/api/scraped-data/
```
```python
#query filter to filter data based on keywords
http://127.0.0.1:8000/api/scraped-data/?keyword=bike
```
```python
#or by date
http://127.0.0.1:8000/api/scraped-data/?date=2023-05-09
```
```python
#or using keywords and dates
http://127.0.0.1:8000/api/scraped-data/?keyword=bike&date=2023-05-09
```
This endpoint will start the scraping
```python
#RUN THE SCRAPING USING ENDPOINT
http://127.0.0.1:8000/api/trigger-scraper
```

## Run Task Scheduler using Celery and RabbitMQ
We also have a feature to scrap the data on every 24 hours. To run this we will need RabbitMQ setup. Follow this link: https://www.rabbitmq.com/download.html to setup it as per device requirements.
Once we have the RabbitMQ running we can trigger the server using these comands.
```python
#navigate to your project directory and start the Celery worker
celery -A amazon_product_scraper worker --loglevel=info
```
```python
#In another terminal window, start the Celery beat
celery -A amazon_product_scraper beat --loglevel=info
```
Make sure to run the commands in separate terminal windows, as they need to run concurrently. The first command starts the Celery worker, which processes the tasks. The second command starts the Celery beat, which schedules tasks to be executed by the worker at specified intervals. In your case, the `trigger_scraper` task will be executed every 24 hours.

## Run Tests
We define some basic Unit tests to check our scrap functions, DB schema and Api endpoints. Which can be test using flowing command.
```python
#Run all tests
python manage.py test
```
