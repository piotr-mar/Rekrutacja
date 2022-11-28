import os
from datetime import timedelta

import requests
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View

from weatherweb.forms import CityForm
from weatherweb.models import WeatherCity


# Create your views here.
class MainView(View):
    """
    Render main view with favourite city if added.
    """
    def get(self, request):
        """
        Render main view.

        :param request: django request
        :return:
        """
        city_weather = None
        if request.user:
            try:
                city_weather = WeatherCity.objects.get(user=request.user)
                self._check_weather_current(city_weather)
            except WeatherCity.DoesNotExist:
                pass
            except TypeError:
                pass
        ctx = {"user": request.user, "data": city_weather}
        return render(request, "main.html", ctx)

    def _check_weather_current(self, city_weather):
        """
        Check if weather data is current.

        :param city_weather: weather object contains data
        :return: None
        """
        self.validate_weather(city_weather)

    def validate_weather(self, weather_data):
        """
        Validate weather data date.

        :param weather_data: weather object contains data
        :return:
        """
        if weather_data.update_at < timezone.now() - timedelta(hours=3):
            weather_data.weather = self._get_weather(weather_data)
            weather_data.forecast = self._get_forecast(weather_data)
            weather_data.save()

    @staticmethod
    def _get_weather(weather_data):
        """
        Get actual weather.

        :param weather_data: weather object contains data
        :return: weather object
        """
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units={}&appid={}"
        units = "metric"
        api_key = os.getenv("API")
        weather = requests.get(url.format(weather_data.lat, weather_data.lon, units, api_key), timeout=10).json()
        return weather

    @staticmethod
    def _get_forecast(weather_data):
        """
        Get forecast

        :param weather_data: weather object contains data
        :return: weather forecast dict
        """
        url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units={}&cnt={}&appid={}"
        cnt = 5
        api_key = os.getenv("API")
        forecast = requests.get(
            url.format(weather_data.lat, weather_data.lon, weather_data.units, cnt, api_key), timeout=10
        ).json()
        forecast["list"] = forecast["list"][8::8]
        return forecast


class CityWeather(View):
    """
    Render city weather search.
    """
    ctx = {}

    def __init__(self, **kwargs):
        """
        Initialize class
        :param kwargs:
        """
        super().__init__(**kwargs)
        self.units = None
        self.lat = None
        self.lon = None
        self.city = None

    def get(self, request):
        """
        Render main view.

        :param request: django request
        :return:
        """
        self.ctx["user"] = request.user
        self.ctx["data"] = None
        self.ctx["form"] = CityForm()
        return render(request, "weather.html", self.ctx)

    def post(self, request):
        """
        Form handler.

        :param request: django request
        :return:
        """
        form = CityForm(request.POST)
        new_city_weather = None

        if form.is_valid():
            self.city = form.cleaned_data["city"]
            self.lon = form.cleaned_data["lon"]
            self.lat = form.cleaned_data["lat"]
            self.units = form.cleaned_data['units']

            db_city = self.check_city_in_db()
            if db_city:
                new_city_weather = db_city
            else:
                new_city_weather = self.fill_form(form, request)

            if "favourite" in request.POST:
                new_city_weather.user = request.user
                new_city_weather.save()
                messages.success(request, "Added to favourites")

        self.ctx["data"] = new_city_weather
        self.ctx["user"] = request.user
        self.ctx["form"] = CityForm(instance=new_city_weather)
        return render(request, "weather.html", self.ctx)

    def fill_form(self, form, request):
        """
        Create new weather object base on form.

        :param form: filled form
        :param request: django request
        :return: new weather object
        """
        new_city_weather = form.save(commit=False)
        if self.city and not (self.lon or self.lat):
            self._get_coordinates_from_city(request)
            new_city_weather.lon = self.lon
            new_city_weather.lat = self.lat
        elif (self.lon and self.lat) and not self.city:
            self._get_city_from_coordinates(request)
            new_city_weather.city = self.city
        new_city_weather.weather = self._get_weather(self.lon, self.lat, self.units)
        new_city_weather.forecast = self._get_forecast(self.lon, self.lat, self.units)
        new_city_weather.save()
        return new_city_weather

    def check_city_in_db(self):
        """
        Check if provided city exist in db.

        :return: weather object
        """
        try:
            weather_city = WeatherCity.objects.filter(
                Q(city=self.city) | Q(lon=self.lon, lat=self.lat)
            ).latest("update_at")
            weather_city = self.validate_weather(weather_city)
        except WeatherCity.DoesNotExist:
            weather_city = None
        return weather_city

    def validate_weather(self, weather_data):
        """
        Validate weather data date.

        :param weather_data: weather object contains data
        :return:
        """
        if weather_data.update_at < timezone.now() - timedelta(hours=3):
            weather_data.weather = self._get_weather(weather_data.lon, weather_data.lat, weather_data.units)
        return weather_data

    @staticmethod
    def _get_forecast(lon, lat, unit,):
        """
        Get forecast.

        :param lon: longitude
        :param lat: latitude
        :param unit: unit
        :return: forecast data
        """
        url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units={}&cnt={}&appid={}"
        cnt = 18
        api_key = os.getenv("API")
        forecast = requests.get(
            url.format(lat, lon, unit, cnt, api_key), timeout=10
        ).json()
        forecast["list"] = forecast["list"][8::8]
        return forecast

    @staticmethod
    def _get_weather(lon, lat, unit):
        """
        Get current weather.

        :param lon: longitude
        :param lat: latitude
        :param unit: unit
        :return: weather data
        """
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units={}&appid={}"
        api_key = os.getenv("API")
        weather = requests.get(url.format(lat, lon, unit, api_key), timeout=10).json()
        return weather

    def _get_city_from_coordinates(self, request):
        """
        Get city base on coordinates.

        :param request: django request
        :return: None or redirect to search page
        """
        url = "http://api.openweathermap.org/geo/1.0/reverse?lat={}&lon={}&limit=1&appid={}"
        api_key = os.getenv("API")
        city = requests.get(url.format(self.lat, self.lon, api_key), timeout=10).json()
        try:
            self.city = city[0]["name"]
            return
        except KeyError:
            messages.error(request, "Error 401 - Wrong API Key")
            return redirect("search")

    def _get_coordinates_from_city(self, request):
        """
        Get coordinates for provided city.

        :param request: django request
        :return: None or redirect to search page
        """
        url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}"
        api_key = os.getenv("API")
        coordinates = requests.get(url.format(self.city, api_key), timeout=10).json()
        try:
            self.lon = coordinates[0]["lon"]
            self.lat = coordinates[0]["lat"]
            return
        except KeyError:
            messages.error(request, "Error 401 - Wrong API Key")
            return redirect("search")
