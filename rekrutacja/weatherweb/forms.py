from django.core.exceptions import ValidationError
from django.forms import ModelForm
from weatherweb.models import WeatherCity


class CityForm(ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('city') and not (cleaned_data.get('lon') or cleaned_data.get('lat')):
            msg = "City name or coordinates must be provided"
            raise ValidationError({"City name or coordinates must be provided"})

    class Meta:
        model = WeatherCity
        fields = ["city", "lon", "lat"]

