from django.contrib.auth import get_user_model
from django.db import models
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

UserModel = get_user_model()
# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}, {self.country}'

    def save(self, *args, **kwargs):
        if (self.latitude is None or self.longitude is None) and self.name and self.country:
            try:
                geolocator = Nominatim(user_agent='wanderwords_dev')
                location = geolocator.geocode(f'{self.name}, {self.country}', timeout=10)
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except GeocoderTimedOut:
              raise ValueError("Geocoding timed out. Please try saving 'destination name, country' again.")
        super().save(*args, **kwargs)