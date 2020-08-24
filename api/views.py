
from weatherapp.models import City
from weatherapp.views import getweather, getforecast
from .serializers import CitySerializer, WeatherSerializer, ForecastSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'cities list': '/city-list/',
        'weather': '/weather/<int:pk>/',
        'forecast': '/forecast/<int:pk>/'
    }
    return Response(api_urls)


@api_view(['GET'])
def citylist_api(request):
    cities = City.objects.all()
    res = CitySerializer(cities, many=True)
    return Response(res.data)


@api_view(['GET'])
def forecast_api(request, cityid):
    try:
        c = City.objects.get(pk=cityid)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        forecast = getforecast(None, c)
        serializer = ForecastSerializer(forecast, many=False, read_only=True)
        return Response(serializer.data)


@api_view(['GET'])
def weather_api(request, cityid):
    try:
        c = City.objects.get(pk=cityid)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        weather = getweather(None, c)
        serializer = WeatherSerializer(weather, many=False, read_only=True)
        return Response(serializer.data)
