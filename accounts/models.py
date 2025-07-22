from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from accounts.managers import WebUserManager


# Create your models here.
class WebUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = WebUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(WebUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=10, validators=[MinLengthValidator(10)],blank=True, null=True)
    backup_email = models.EmailField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)

    @property
    def full_name(self):
        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()
        return full_name if full_name else None

    def clean(self):
        super().clean()
        if self.backup_email and self.backup_email == self.user.email:
            raise ValidationError({
                'backup_email': 'Your backup email cannot be the same as your account email!',
            })
