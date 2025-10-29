from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
UserModel = get_user_model()

class TestUserModel(TestCase):
    def setUp(self):
        self.username='TesUsername'
        self.password='testmaintest'
        self.email = 'teast@main.com'

        self.user = UserModel.objects.create_user(
            username = self.username,
            email = self.email,
            password = self.password
        )

    def test_valid_str_method_returns_username(self):
            self.assertEqual('TesUsername', str(self.user))