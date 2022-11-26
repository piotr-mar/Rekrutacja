import os
import requests

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from weatherweb.forms import CityForm


# Create your views here.


def index(request):
    return render(request, "index.html", {})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Successfully login."))
            return redirect("main")
        else:
            messages.success(request, ("Error during login. Try again."))
            return redirect("login")
    return render(request, 'user/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Successfuly logout"))
    return redirect('main')


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("Successfuly register and login"))
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, "user/register.html", {'form': form})


class CityWeather(View):
    form = CityForm()
    ctx = {"form": form}

    def get(self, request):
        return render(request, "main.html", self.ctx)

    def post(self, request):
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            lon = form.cleaned_data['lon']
            lat = form.cleaned_data['lat']
            new_city_weather = form.save(commit=False)

            if city and not (lon or lat):
                lon, lat = self._get_coordinates(city)
                new_city_weather['lon'] = lon
                new_city_weather['lat'] = lat

            if (lon or lat) and not city:
                city = self._get_city(lon, lat)
                new_city_weather['city'] = city

            form.save()
            self.ctx['weather'] = self._get_weather(lon, lat)
            self.ctx['city'] = city
            return render(request, "main.html", self.ctx)

    def _get_weather(self, lon, lat):
        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={dfdd54bdbd96419492c27b9d97d9366b}"
        units = "metric"
        api_key = os.getenv('API')
        weather = requests.get(url.format(lat, lon, units, api_key)).json()
        return weather

    def _get_city(self, lon, lat):
        url = "http://api.openweathermap.org/geo/1.0/reverse?lat={}&lon={}&limit=1&appid={}"
        api_key = os.getenv('API')
        city = requests.get(url.format(lat, lon, api_key)).json()
        return city[0]["name"]

    def _get_coordinates(self, city):
        url = "http://api.openweathermap.org/geo/1.0/direct?q={}&limit=1&appid={}"
        api_key = os.getenv('API')
        coordinates = requests.get(url.format(city, api_key)).json()
        return coordinates[0]['lon'], coordinates[0]["lat"]

    def _check_form_fields(self):
        pass

# def get_city_weather(request):
#     if request.method == 'POST':
#         pass
#     form = CityForm()
#     ctx = {"form": form}
#     return render(request, "main.html", ctx)