from rest_framework import serializers
from weatherapp.models import City, Weather, Forecast

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name_ru', 'name_en', 'name_uk', 'country', 'state', 'coord_lon', 'coord_lat']

class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = ['city', 'loadingtime', 'forecastdata']

class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = ['city', 'loadingtime', 'weatherdata']