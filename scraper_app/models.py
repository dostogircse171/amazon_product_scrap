from django.utils import timezone
from django.db import models


class Keyword(models.Model):
    word = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.word


class ScrapedData(models.Model):
    title = models.CharField(max_length=255)
    link = models.TextField()
    sponsored = models.BooleanField(default=False)
    price = models.CharField(max_length=255, null=True)
    description = models.TextField()
    rating = models.CharField(max_length=255, null=True)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    date_scraped = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
