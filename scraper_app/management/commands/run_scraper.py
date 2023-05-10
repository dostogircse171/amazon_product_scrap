from django.core.management.base import BaseCommand
from scraper_app.product_scraper import run_scraper

# creating a  custom command to run the scraper.
# Although we have an API endpoint to run the scraper, we can also run it from the command line.
# python manage.py run_scraper


class Command(BaseCommand):
    help = 'Runs the Amazon scraper for the keywords in the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting the scraper...'))
        run_scraper()
        self.stdout.write(self.style.SUCCESS('Scraper finished successfully.'))
