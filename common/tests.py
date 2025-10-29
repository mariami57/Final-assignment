from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from books.models import Book
from destinations.models import Destination
from posts.models import Post

# Create your tests here.
UserModel = get_user_model()


class ModelTests(TestCase):

    def create_test_image(self, name='test_image.jpg', size=(100, 100), color=(255, 0, 0)):
        file_obj = BytesIO()
        image = Image.new('RGB', size=size, color=color)
        image.save(file_obj, 'JPEG')
        file_obj.seek(0)
        return SimpleUploadedFile(name, file_obj.read(), content_type='image/jpeg')

    def setUp(self):
        test_image = self.create_test_image()
        self.user = UserModel.objects.create(username='testuser', password='12345')
        self.dest = Destination.objects.create(name='Alaska', country='USA', created_by=self.user, latitude=63.5888,
                                               longitude=154.4931)
        self.book = Book.objects.create(title='Into the Wild', author='Jon Krakauer', genre='Biography',
                                        added_by=self.user)
        self.post = Post.objects.create(user=self.user, book=self.book, destination=self.dest,
                                        content='It was cold but beautiful!',
                                        title='My Alaska Trip', image1=test_image)

    def test_search_returns_results(self):
        response = self.client.get('/api/search/?q=Alaska')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cold', str(response.content))
