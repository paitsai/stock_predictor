from django.urls import path, include
from rest_framework.routers import DefaultRouter

from predictor import views


router = DefaultRouter()
router.register('stocks_all', views.StockViewSet)

urlpatterns = [
    path('stocks_all/', include(router.urls)),
    path('get_stocks_prices_by_code/<str:company_code>/', views.GetStockPriceByCompanyCode.as_view(), name='get-stock-price'),
    path('get_stocks_all_list/<int:company_num>/<int:stock_num>/', views.FetchSomeStockInfo.as_view(), name='fetch_some_stock_codes'),
    path('register/', views.RegistrationAPIView.as_view(), name='user-register'),
]
