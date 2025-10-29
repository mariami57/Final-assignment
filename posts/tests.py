from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory

from books.models import Book
from destinations.models import Destination
from posts.mixins import BookDestinationHandlerMixin
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
        self.user = UserModel.objects.create_user(username='testuser', password='12345')
        self.dest = Destination.objects.create(name='Alaska', country='USA', created_by=self.user, latitude=63.5888,
                                               longitude=154.4931)
        self.book = Book.objects.create(title='Into the Wild', author='Jon Krakauer', genre='Biography',
                                        added_by=self.user)
        self.post = Post.objects.create(user=self.user, book=self.book, destination=self.dest,
                                        content='It was cold but beautiful!',
                                        title='My Alaska Trip', image1=test_image)

    def test_post_str_returns_title(self):
        self.assertEqual(str(self.post), "My Alaska Trip")




class DummyForm:
    def __init__(self, cleaned_data, instance = None):
        self.cleaned_data = cleaned_data
        self.instance = instance or type('Instance', (), {'pk':None})()

class TestBookDestinationHandlerMixin(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="tester", password="12345")
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = self.user
        self.mixin = BookDestinationHandlerMixin()
        self.mixin.request = self.request

    def test_creates_new_book_and_new_destination_when_choice_is_other(self):
        form = DummyForm({
            'book_choice': 'other',
            'book_title': 'Wanderlust Tales',
            'destination_choice': 'other',
            'destination_name': 'Kyoto',
            'destination_country': 'Japan',
            'latitude': 35.6895,
            'longitude': 139.6917,
        })

        book, destination = self.mixin.handle_book_and_destination(form)

        self.assertIsNotNone(book)
        self.assertIsNotNone(destination)
        self.assertEqual(destination.name, 'Kyoto')
        self.assertIn(destination, book.destinations.all())


    def test_uses_existing_book_and_destination_when_choices_given(self):
        existing_book = Book.objects.create(title="Old Book", author="Author", genre="Genre", added_by=self.user)
        existing_dest = Destination.objects.create(
            name="Paris", country="France", latitude=48.8566, longitude=2.3522, created_by=self.user
        )

        form = DummyForm({
            'book_choice': existing_book.id,
            'book_title': '',
            'destination_choice': existing_dest.id,
            'destination_name': '',
            'destination_country': '',
            'latitude': None,
            'longitude': None,
        })

        book, destination = self.mixin.handle_book_and_destination(form)

        self.assertEqual(book, existing_book)
        self.assertEqual(destination, existing_dest)
        self.assertIn(existing_dest, existing_book.destinations.all())

    def test_edit_mode_adds_existing_destination_to_book(self):
        book = Book.objects.create(title="TestBook", author="A", genre="G", added_by=self.user)
        dest = Destination.objects.create(
            name="Lisbon", country="Portugal", latitude=38.7223, longitude=-9.1393, created_by=self.user
        )

        instance = type('Instance', (), {'pk':1})()

        form = DummyForm({
            'book_choice': book.id,
            'book_title': '',
            'destination_choice': dest.id,
            'destination_name': '',
            'destination_country': '',
            'latitude': None,
            'longitude': None,
        }, instance=instance)


        book, destination = self.mixin.handle_book_and_destination(form)

        self.assertIn(dest, book.destinations.all())