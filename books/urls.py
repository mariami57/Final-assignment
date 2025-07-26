from django.urls import path, include

from books.views import GenreBooksListView, BooksByGenreListView

urlpatterns = [

    path('genres/', GenreBooksListView.as_view(), name='genres-list'),
    path('<path:genre>/', BooksByGenreListView.as_view(), name='books-by-genre'),

]