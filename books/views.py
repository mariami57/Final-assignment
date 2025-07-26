from collections import defaultdict
from django.views.generic import ListView
from books.models import Book

# Create your views here.
class GenreBooksListView(ListView):
    model = Book
    template_name = 'book/genres-list.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        grouped_books = defaultdict(list)

        for book in Book.objects.all():
            genre = book.genre if book.genre is not None else 'Undefined'
            grouped_books[genre].append(book)

        context['grouped_books'] = dict(grouped_books)

        return context

class BooksByGenreListView(ListView):
    model = Book
    template_name = 'book/books-by-genre.html'

    def get_queryset(self):
        genre_param = self.kwargs['genre']
        if genre_param.lower() == 'undefined':
            return Book.objects.filter(genre__isnull=True)
        return Book.objects.filter(genre=genre_param)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genre_param = self.kwargs['genre']
        context['genre'] = 'Undefined' if genre_param.lower() == 'undefined' else genre_param
        return context
