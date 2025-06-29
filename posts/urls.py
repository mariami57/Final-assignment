from django.urls import path

from posts.views import PostFeedView

urlpatterns = [
    path('posts-feed/', PostFeedView.as_view(), name='posts-feed'),
]