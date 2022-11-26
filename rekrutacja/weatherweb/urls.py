from django.urls import path
from . import views
from .views import CityWeather

urlpatterns = [
    path("", CityWeather.as_view(), name='main'),
    path("login", views.login_user, name='login'),
    path("logout", views.logout_user, name='logout'),
    path("register", views.register_user, name='register'),
]