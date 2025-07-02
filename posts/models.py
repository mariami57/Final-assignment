from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.CharField(max_length=50)
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