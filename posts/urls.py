from django.urls import path

from posts.views import PostFeedView, AddPostView

urlpatterns = [
    path('posts-feed/', PostFeedView.as_view(), name='posts-feed'),
    path('add/', AddPostView.as_view(), name='add-post'),
]