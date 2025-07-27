import json

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Final_assignment.serializers import PostSerializer, BookSerializer, ProfileSerializer
from accounts.models import Profile
from books.models import Book
from posts.models import Post, UserModel

UserModel = get_user_model()
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

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from accounts.models import Profile
from books.models import Book

from posts.models import Post

class GlobalSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        results = []

        if query:

            profiles = Profile.objects.filter(
                Q(user__username__icontains=query) |
                Q(first_name__icontains=query)
            )
            books = Book.objects.filter(title__icontains=query)
            posts = Post.objects.filter(title__icontains=query)


            profile_data = ProfileSerializer(profiles, many=True).data
            for item in profile_data:
                item['label'] = f"User: {item['username']}"
            results.extend(profile_data)

            book_data = BookSerializer(books, many=True).data
            for item in book_data:
                item['label'] = f"Book: {item['title']}"
            results.extend(book_data)


            post_data = PostSerializer(posts, many=True).data
            for item in post_data:
                item['label'] = f"Post: {item['title']}"
            results.extend(post_data)

        return Response(results)


