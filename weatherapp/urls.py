from . import views
from .views import CityAutocomplete

from django.urls import path


app_name = 'weatherapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('addcityform/', views.addcityform, name='addcityform'),
    path('addcity/<int:city_id>', views.addcity, name='addcity'),
    path('deletecity/<int:city_id>', views.deletecity, name='deletecity'),
    path('dosm/', views.dosm, name='dosm'),
    path('dbvacuum/', views.vacuum_db, name='vacuum_db'),
    path('forecast/<int:city_id>', views.forecast, name='forecast'),
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete')
]




