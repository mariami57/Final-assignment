from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from accounts.forms import CustomLoginForm
from accounts.views import SignInView, ProfileDetailView, ProfileEditView

urlpatterns = [
    path('accounts/', include([
        path('signin/', SignInView.as_view(), name='signin'),
        path('login/', LoginView.as_view(template_name='accounts/log-in.html', authentication_form=CustomLoginForm),
             name='login'),
        path('logout/', LogoutView.as_view(), name='logout'),
        path('profile/<int:pk>/', include([
            path('profile-details/', ProfileDetailView.as_view(), name='profile-details-page'),
            path('profile-edit/', ProfileEditView.as_view(), name='profile-edit'),
        ])),
    ]))

]