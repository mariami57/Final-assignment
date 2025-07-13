from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import WebUserCreationForm


# Create your views here.
class SignInView(CreateView):
    form_class = WebUserCreationForm
    template_name = 'accounts/sign-in.html'
    success_url = reverse_lazy('posts-feed')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully registered! Please log in.')
        return response