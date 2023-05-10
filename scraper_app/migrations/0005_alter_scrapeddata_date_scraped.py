# Generated by Django 4.2.1 on 2023-05-09 22:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("scraper_app", "0004_alter_scrapeddata_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scrapeddata",
            name="date_scraped",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
