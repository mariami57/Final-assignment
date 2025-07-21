from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import WebUser, Profile

UserModel = get_user_model()

class WebUserCreationForm(UserCreationForm):
    class Meta:
        model = WebUser
        fields = ('username', 'email')


class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Oops! The username or password is incorrect. Please try again."
        ),
        'inactive': _("This account is inactive."),
    }

class ProfileBaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

class ProfileEditForm(ProfileBaseForm):
    class Meta(ProfileBaseForm.Meta):
        fields = ('first_name', 'last_name', 'phone_number', 'backup_email', 'profile_picture')

