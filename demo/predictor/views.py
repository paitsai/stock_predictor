from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count
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
    # 根据Company Code来获取
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
        

class FetchSomeStockInfo(generics.RetrieveAPIView):
    queryset = StockPrice.objects.all()
    serializer_class = StockSerializer

    def get(self, request, company_num, stock_num):
        try:
            # Fetch a limited number of distinct company codes
            company_codes = StockPrice.objects.values('company_code').annotate(count=Count('id')).filter(count__gt=0)
            print("Distinct Company Codes:", list(company_codes))  # 打印出所有不同的公司代码
            
            distinct_company_codes = [code['company_code'] for code in company_codes][:company_num]
            print("Filtered Distinct Company Codes:", distinct_company_codes)  # 打印过滤后的公司代码
            
            if distinct_company_codes:
                stock_prices_data = {}
                
                for code in distinct_company_codes:
                    print(f"Fetching prices for company code: {code}")  # Debug output
                    recent_stock_prices = StockPrice.objects.filter(company_code=code).order_by('-date')[:stock_num]
                    print(f"Recent prices for {code}:", recent_stock_prices)  # Debug output
                    serializer = self.get_serializer(recent_stock_prices, many=True)
                    stock_prices_data[code] = serializer.data
                
                return Response(stock_prices_data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No company codes found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def IndexPage(request):
    return render(request, 'index.html')

def StocksPage(request):
    return render(request, 'companyList.html')

