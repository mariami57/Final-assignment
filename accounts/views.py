from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import WanderWordsUserCreationForm


# Create your views here.
class SignInView(CreateView):
    form_class = WanderWordsUserCreationForm
    template_name = 'accounts/sign-in.html'
    success_url = reverse_lazy('posts')