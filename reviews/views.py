from django.db.models import Avg, Count
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.book = None
        if 'book_pk' in kwargs:
            self.book = get_object_or_404(Book, pk=kwargs['book_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = self.book

        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.book:
            form.fields['book'].initial = self.book
            form.fields['book'].disabled = True
        return form

    def form_valid(self, form):
        if not self.book:
            self.book = form.cleaned_data.get('book')
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
        self.book = get_object_or_404(Book, pk=book_pk)
        context['book_pk'] = book_pk
        context['book'] = self.book
        aggregated = Review.objects.filter(book=self.book).aggregate(
            reviews_count=Count('id'),
            avg_rating=Avg('rating'),
        )
        context.update({
            'reviews_count':aggregated['reviews_count'],
            'avg_rating': round(aggregated['avg_rating']) or 0
        })

        user = self.request.user
        context['has_reviewed'] = Review.objects.filter(book__pk=book_pk).filter(user=user).exists()
        return context



