from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from scraper_app.models import Keyword, ScrapedData
from .serializers import KeywordSerializer, ScrapedDataSerializer
from scraper_app.product_scraper import run_scraper


class ScrapedDataList(generics.ListAPIView):
    queryset = ScrapedData.objects.all()
    serializer_class = ScrapedDataSerializer

    def get_queryset(self):
        queryset = ScrapedData.objects.all()
        keyword = self.request.query_params.get('keyword', None)
        date = self.request.query_params.get('date', None)

        if keyword is not None:
            queryset = queryset.filter(keyword__word__icontains=keyword)

        if date is not None:
            queryset = queryset.filter(date_scraped__date=date)

        return queryset


class TriggerScraper(APIView):
    def get(self, request):
        run_scraper()
        return Response({"status": "Scraper started successfully."})
