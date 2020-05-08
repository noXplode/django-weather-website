from django.db import models
from .fields import JSONField
from django.utils import timezone

class City(models.Model):
    name = models.CharField(max_length=100)
    opw_id = models.IntegerField(default=0)
    country = models.CharField(max_length=80, default='')
    state = models.CharField(max_length=80, default='')
    coord_lon = models.DecimalField(max_digits=12, decimal_places=6, default=0)
    coord_lat = models.DecimalField(max_digits=12, decimal_places=6, default=0)

    def __str__(self):
        return self.name

class Forecast(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    loadingtime = models.DateTimeField(auto_now_add=True)
    forecastdata = JSONField()

    class Meta:
        ordering = ['-loadingtime']

    def __str__(self):
        return f'{self.cityid.name} {self.loadingtime.strftime("%d/%m/%Y, %H:%M:%S")}'

    def is_actual(self):
        timediff = timezone.now() - self.loadingtime
        if timediff.seconds <= 3600:
            return True
        else:
            return False

class Popularity(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=False)
    pickeddate = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pickeddate']

    def __str__(self):
        return self.cityid.name

   

