from django.contrib.auth import get_user_model
from django.db import models

from books.models import Book
from destinations.models import Destination

UserModel = get_user_model()
# Create your models here.
class Post(models.Model):
    user=models.ForeignKey(UserModel, on_delete=models.CASCADE)
    book=models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    destination=models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    image1 = models.ImageField(upload_to='post_mediafiles/', blank=True,null=True)
    image2 = models.ImageField(upload_to='post_mediafiles/', blank=True, null=True)
    image3 = models.ImageField(upload_to='post_mediafiles/', blank=True, null=True)

    @property
    def image_count(self):
        count = 0
        if self.image1:
            count += 1
        if self.image2:
            count += 1
        if self.image3:
            count += 1
        return count