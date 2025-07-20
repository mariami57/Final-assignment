from django.contrib.auth import get_user_model
from django.db import models


UserModel = get_user_model()
# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.name}, {self.country}"