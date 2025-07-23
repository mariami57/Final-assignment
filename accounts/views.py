from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView

from accounts.forms import WebUserCreationForm, ProfileEditForm
from accounts.models import Profile
from destinations.models import Destination, UserModel


# Create your views here.
UserModel = get_user_model()
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
    form_class = ProfileEditForm
    template_name = 'accounts/edit-profile.html'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Your profile information has been successfully updated!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile-edit', kwargs={'pk': self.object.pk})


@login_required
def profile_delete_view(request, pk):
    user = UserModel.objects.get(pk=pk)
    if request.user.is_authenticated and request.user.pk == user.pk:
        if request.method == 'POST':
            user.delete()
            messages.success(request, 'Your profile has been successfully deleted!')
            return redirect('home')
    else:
        messages.error(request, 'You are not authorized to delete this profile.')
        return redirect('profile-details-page', pk=pk)

    return redirect('profile-details-page', pk=pk)
