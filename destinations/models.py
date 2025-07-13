from django.db import models

# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f" {self.name}, {self.country}"