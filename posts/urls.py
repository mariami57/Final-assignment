from django.urls import path, include

from accounts.views import ProfileDetailView
from posts.views import PostFeedView, AddPostView, PostEditView, post_delete_view, PostDetailView

urlpatterns = [
    path('posts-feed/', PostFeedView.as_view(), name='posts-feed'),
    path('add/', AddPostView.as_view(), name='add-post'),
    path('<int:pk>/', include([
        path('edit/', PostEditView.as_view(), name='post-edit'),
        path('delete/', post_delete_view, name='post-delete'),

        path('details/', PostDetailView.as_view(), name='post-details'),
    ]))
]