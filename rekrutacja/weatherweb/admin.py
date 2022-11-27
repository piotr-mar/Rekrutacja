from django.contrib import admin

from weatherweb.models import WeatherCity


# Register your models here.

class WeatherAdmin(admin.ModelAdmin):
    list_display = ['city', 'lon', 'lat', 'user', "metric", 'create_at', 'update_at']


admin.site.register(WeatherCity, WeatherAdmin)
