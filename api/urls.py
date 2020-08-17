from . import views
from django.urls import path

app_name = 'api'
urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('city-list/', views.citylist_api, name='citylist'),
    path('weather/<str:cityid>/', views.weather_api, name='weather'),
    path('forecast/<str:cityid>/', views.forecast_api, name='forecast'),
]




