from django.urls import path, include

from books.views import GenreBooksListView

urlpatterns = [

    path('genres-list/', GenreBooksListView.as_view(), name='genres-list'),

]