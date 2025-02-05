from django.urls import path, include
from rest_framework.routers import DefaultRouter

from predictor import views


router = DefaultRouter()
router.register('stocks_all', views.StockViewSet)

urlpatterns = [
    path('stocks_all/', include(router.urls)),
    path('get_stocks_prices_by_code/<str:company_code>/', views.GetStockPriceByCompanyCode.as_view(), name='get-stock-price'),
]
