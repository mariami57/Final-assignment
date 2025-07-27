import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
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

@require_http_methods(["GET", "POST"])
def save_cookie_preferences(request):
    if request.method == "POST":
        data = json.loads(request.body)
        request.session['cookies_preference'] = data
        return JsonResponse({'message': 'Preferences saved'})
    else:
        preferences = request.session.get('cookies_preferences', {})
        return JsonResponse(preferences)