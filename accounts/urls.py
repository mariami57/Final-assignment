from django.urls import path

from accounts.views import SignInView

urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='sign-in'),
]