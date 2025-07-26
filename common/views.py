from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomeView(TemplateView):
    template_name = 'common/home.html'

def contacts_page_view(request):
    return render(request, 'common/contacts.html')

def help_page_view(request):
    return render(request, 'common/help.html')

def cookies_page_view(request):
    return render(request, 'common/cookies.html')