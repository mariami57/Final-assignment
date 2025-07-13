from django.contrib.auth import get_user_model
from django.db import models

from destinations.models import Destination

UserModel = get_user_model()
# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, null=True, blank=True)
    destinations = models.ManyToManyField(Destination, related_name='books')
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='books_added')

    def __str__(self):
        return self.title
