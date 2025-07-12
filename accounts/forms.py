from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import WanderWordsUser

UserModel = get_user_model()

class WanderWordsUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = WanderWordsUser
        fields = ('username', 'email')