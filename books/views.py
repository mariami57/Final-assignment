# Create your views here.
from django.views.generic import ListView

from books.models import Book



class GenreBooksListView(ListView):
    model = Book
    template_name = 'book/genres-list.html'

