from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import WebUserCreationForm
from accounts.models import Profile
from destinations.models import Destination


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

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile-details-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_count'] =self.object.user.post_set.values('book').count()
        context['destination_count'] =self.object.user.post_set.values('destination').distinct().count()
        destination_ids = self.object.user.post_set.values_list('destination', flat=True).distinct()
        context['visited_destinations'] = Destination.objects.filter(id__in=destination_ids)

        return context

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    template_name = 'accounts/edit-profile.html'
