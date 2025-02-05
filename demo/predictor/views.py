from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from predictor.models import StockPrice
from predictor.serializer import StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all()
    serializer_class = StockSerializer


class GetStockPriceByCompanyCode(generics.RetrieveAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockSerializer
    
    def get(self, request, company_code):
        try:
            stock_prices = StockPrice.objects.filter(company_code=company_code)
            if stock_prices.exists():
                serializer = self.get_serializer(stock_prices, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)