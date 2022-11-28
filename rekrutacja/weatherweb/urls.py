from django.urls import path
from .views import CityWeather, MainView

urlpatterns = [
    path("search", CityWeather.as_view(), name="search"),
    path("", MainView.as_view(), name="main"),
]
