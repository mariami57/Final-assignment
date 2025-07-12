from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.forms import CustomLoginForm
from accounts.views import SignInView

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('login/', LoginView.as_view(template_name='accounts/log-in.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]