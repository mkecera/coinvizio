from django.conf.urls import url
from . import views


app_name = 'dashboard'

urlpatterns = [
 # /dashboard/
 url(r'^$', views.index, name='index'),
 # /dashboard/12
 url(r'^(?P<coinId>[0-9]+)/$', views.detail, name='detail'),
 # data market cap
 url(r'^chart/dataMarketCap/', views.pieChartDataCoinMarketCap.as_view()),
 # data 24h change 
 url(r'^chart/data24hChange/', views.barChartData24hChange.as_view()),
 # data 24h top capitalisation coins change
 url(r'^chart/dataTopCapChange/', views.barChartDataTopCapChange.as_view()),
 ]