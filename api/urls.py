from . import views
from django.urls import path

app_name = 'api'
urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
]




