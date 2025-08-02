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
    created_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.country}'
