from django.urls import path
from . import views
from .views import CityWeather

urlpatterns = [
    path("", CityWeather.as_view(), name='main'),
]