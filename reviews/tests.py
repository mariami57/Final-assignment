from django.contrib.auth import get_user_model
from django.test import TestCase

from books.models import Book
from reviews.models import Review

# Create your tests here.
UserModel = get_user_model()
class TestReview(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username='reviewer', password='reviewer1')
        self.book = Book.objects.create(title='Tuscan Spring', author='Sandro Botticelli', genre='Biography',
                                        added_by=self.user)
        self.review = Review.objects.create(user=self.user, book=self.book,
                    content='Beautiful vineyards and rolling hills.', rating='5')

    def test_review_str_return_string(self):

        self.assertEqual("'Tuscan Spring' Review", str(self.review))

