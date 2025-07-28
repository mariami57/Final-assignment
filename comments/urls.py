from django.urls import path, include

from comments import views

urlpatterns = [
    path('<int:pk>/', include([
        path('edit/', views.edit_comment, name='comment-edit'),
        path('delete/', views.delete_comment, name='comment-delete'),
    ]))
]