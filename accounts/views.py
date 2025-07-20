from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from accounts.forms import WebUserCreationForm
from accounts.models import Profile


# Create your views here.
class SignInView(CreateView):
    form_class = WebUserCreationForm
    template_name = 'accounts/sign-in.html'
    success_url = reverse_lazy('posts-feed')
    #Uses signal to create a profile for the user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have successfully registered! Please log in.')
        return response

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_count'] =self.object.user.post_set.values('book').count()
        context['destination_count'] =self.object.user.post_set.values('destination').distinct().count()


        return context