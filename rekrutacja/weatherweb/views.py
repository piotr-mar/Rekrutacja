import os

import requests
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View

from weatherweb.forms import CityForm
from weatherweb.models import WeatherCity


# Create your views here.

class CityWeather(View):
    form = CityForm()
    ctx = {"form": form}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lat = None
        self.lon = None
        self.city = None

    def get(self, request):
        return render(request, "weather.html", self.ctx)

    def post(self, request):
        form = CityForm(request.POST)
        new_city_weather = None

        if form.is_valid():
            self.city = form.cleaned_data['city']
            self.lon = form.cleaned_data['lon']
            self.lat = form.cleaned_data['lat']

            db_city = self.check_city_in_db()
            if db_city:
                new_city_weather = db_city
            else:
                new_city_weather = form.save(commit=False)
                if 'favourite' in request.POST:
                    new_city_weather.user = request.user
                    messages.success(request, "Added to favourites")
                else:
                    if self.city and not (self.lon or self.lat):
                        self._get_coordinates_from_city(request)
                        new_city_weather.lon = self.lon
                        new_city_weather.lat = self.lat

                    elif (self.lon and self.lat) and not self.city:
                        self._get_city_from_coordinates(request)
                        new_city_weather.city = self.city

                new_city_weather.weather = self._get_weather()
                new_city_weather.forecast = self._get_forecast()
                new_city_weather.save()

        self.ctx['data'] = new_city_weather
        self.ctx['form'] = CityForm(instance=new_city_weather)
        return render(request, "weather.html", self.ctx)

    def check_city_in_db(self):
        try:
            weather_city = WeatherCity.objects.filter(Q(city=self.city) | Q(lon=self.lon, lat=self.lat)).latest('update_at')
        except WeatherCity.DoesNotExist:
            weather_city = None
        return weather_city

    def _get_forecast(self):
        url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units={}&cnt={}&appid={}'
        units = "metric"
        cnt = 5
        api_key = os.getenv('API')
        forecast = requests.get(url.format(self.lat, self.lon, units, cnt, api_key)).json()
        return forecast

    def _get_weather(self):
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units={}&appid={}"
        units = "metric"
        api_key = os.getenv('API')
        weather = requests.get(url.format(self.lat, self.lon, units, api_key)).json()
        return weather

    def _get_city_from_coordinates(self, request):
        url = "http://api.openweathermap.org/geo/1.0/reverse?lat={}&lon={}&limit=1&appid={}"
        api_key = os.getenv('API')
        city = requests.get(url.format(self.lat, self.lon, api_key)).json()
        try:
            self.city = city[0]["name"]
        except KeyError:
            messages.error(request, "Error 401 - Wrong API Key")
            return redirect('main')

    def _get_coordinates_from_city(self, request):
        url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}"
        api_key = os.getenv('API')
        coordinates = requests.get(url.format(self.city, api_key)).json()
        try:
            self.lon = coordinates[0]['lon']
            self.lat = coordinates[0]["lat"]
        except KeyError:
            messages.error(request, "Error 401 - Wrong API Key")
            return redirect('main')
