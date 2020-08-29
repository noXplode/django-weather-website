from . import views
from django.urls import path

app_name = 'api'
urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('city-list/', views.citylist_api, name='citylist'),
    path('weather/<str:city>/', views.weather_api, name='weather'),
    path('forecast/<int:cityid>/', views.forecast_api, name='forecast'),
]
