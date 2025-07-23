from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from books.models import Book
from reviews.forms import CreateReviewForm
from reviews.models import Review


# Create your views here.
class CreateReviewView(CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = 'reviews/add-review.html'


    def dispatch(self, request, *args, **kwargs):
        self.book = get_object_or_404(Book, pk=kwargs['book_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book

        return context

    def form_valid(self, form):
        form.instance.book = self.book
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('reviews-list', kwargs={'book_pk': self.book.pk})

class ReviewsPerBookView(ListView):
    model = Review
    template_name = 'reviews/reviews-list.html'

    def get_queryset(self):
        book_pk = self.kwargs.get('book_pk')
        return Review.objects.filter(book__pk=book_pk).select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_pk = self.kwargs.get('book_pk')
        context['book_pk'] = book_pk
        context['book'] = get_object_or_404(Book, pk=self.kwargs.get('book_pk'))
        return context

