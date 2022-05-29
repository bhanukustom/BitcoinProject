from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BitCoinPrice, BitcoinPriceSerializer
from .custom_pagination import PricePagination


class PricingAPI(APIView, PricePagination):
    def _validate_date_format(self, query_date):
        try:
            query_date = datetime.strptime(query_date, "%d-%m-%Y")
            query_date = query_date.strftime("%Y-%m-%d")
            return query_date
        except ValueError:
            return False

    def get(self, req):
        query_date = req.GET.get('date')
        if not query_date:
            return Response(status=400, data={"message": "Missing required parameter, `date`."})
        query_date = self._validate_date_format(query_date)
        if not query_date:
            return Response(status=400, data={"message": "Invalid date format. Expected format=DD-MM-YYYY"})
        # fetch
        btc_prices = BitCoinPrice.objects.filter(timestamp__date=query_date)
        # paginate
        results = self.paginate_queryset(btc_prices, req, view=self)
        # serialize
        serialized_prices = BitcoinPriceSerializer(results, many=True)
        return self.get_paginated_response(serialized_prices.data)


