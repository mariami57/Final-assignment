from django.urls import path, include

from posts.views import PostFeedView, AddPostView, PostEditView

urlpatterns = [
    path('posts-feed/', PostFeedView.as_view(), name='posts-feed'),
    path('add/', AddPostView.as_view(), name='add-post'),
    path('<int:pk>/', include([
        path('edit/', PostEditView.as_view(), name='post-edit'),
    ]))
]