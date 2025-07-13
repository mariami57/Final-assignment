from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from accounts.models import WebUser

UserModel = get_user_model()

class WebUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WebUser
        fields = ('username', 'email')




class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Oops! The username or password is incorrect. Please try again."
        ),
        'inactive': _("This account is inactive."),
    }