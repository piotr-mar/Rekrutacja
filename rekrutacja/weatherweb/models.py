from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class WeatherCity(models.Model):
    city = models.CharField(max_length=128, blank=True)
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    metric = models.CharField(max_length=16, choices=[('metric', 'metric'), ('imperial', 'imperial')], null=True,
                              blank=True)
    weather = models.JSONField(blank=True, null=True)
    forecast = models.JSONField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
