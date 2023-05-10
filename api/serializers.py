from rest_framework import serializers
from scraper_app.models import Keyword, ScrapedData

# Create Keyword serializers to convert model data into JSON format


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['word']

# Create ScrapedData serializers to convert model data into JSON format


class ScrapedDataSerializer(serializers.ModelSerializer):
    keyword = KeywordSerializer()

    class Meta:
        model = ScrapedData
        fields = ['title', 'link', 'sponsored', 'price',
                  'description', 'rating', 'keyword', 'date_scraped']
