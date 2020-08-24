from django.db import models
from .fields import JSONField
from django.utils import timezone
from django.urls import reverse

from datetime import timedelta


class City(models.Model):
    name = models.CharField(max_length=100)
    opw_id = models.IntegerField(default=0)
    country = models.CharField(max_length=80, default='')
    state = models.CharField(max_length=80, default='')
    coord_lon = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    coord_lat = models.DecimalField(max_digits=12, decimal_places=6, default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.country} ({round(self.coord_lon,2)}, {round(self.coord_lat,2)})'

    def get_absolute_url(self):     # used in xml sitemap
        return reverse('weatherapp:forecast', args=[str(self.pk)])

    def get_actual_weather(self):
        if self.weather_set.all().exists():
            w = self.weather_set.all().order_by('-loadingtime')[0]
            if w.is_actual():
                return w

    def get_actual_forecast(self):
        if self.forecast_set.all().exists():
            f = self.forecast_set.all().order_by('-loadingtime')[0]
            if f.is_actual():
                return f


class Weather(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    loadingtime = models.DateTimeField(auto_now_add=True)
    weatherdata = JSONField()

    class Meta:
        ordering = ['-loadingtime']

    def __str__(self):
        return f'{self.city.name} {self.loadingtime.strftime("%d/%m/%Y, %H:%M:%S")}'

    def is_actual(self):
        timediff = timezone.now() - self.loadingtime
        if timediff <= timedelta(seconds=1800):
            return True
        else:
            return False


class Forecast(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    loadingtime = models.DateTimeField(auto_now_add=True)
    forecastdata = JSONField()
    citydata = JSONField(default='')

    class Meta:
        ordering = ['-loadingtime']

    def __str__(self):
        return f'{self.city.name} {self.loadingtime.strftime("%d/%m/%Y, %H:%M:%S")}'

    def is_actual(self):
        timediff = timezone.now() - self.loadingtime
        if timediff <= timedelta(seconds=3600):
            return True
        else:
            return False


class Popularity(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    pickeddate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pickeddate']

    def __str__(self):
        return self.city.name
