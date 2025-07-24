from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from books.models import Book


UserModel = get_user_model()
# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    date_added = models.DateTimeField(auto_now_add=True)