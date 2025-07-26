from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from books.models import Book
from common.mixins import UserIsCreatorMixin
from reviews.forms import CreateReviewForm, EditReviewForm
from reviews.models import Review


# Create your views here.
class CreateReviewView(LoginRequiredMixin, CreateView):
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

class ReviewsPerBookView(LoginRequiredMixin, ListView):
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
        avg_rating_raw = aggregated['avg_rating']
        avg_rating = round(avg_rating_raw, 2) if avg_rating_raw is not None else 0
        context.update({
            'reviews_count':aggregated['reviews_count'],
            'avg_rating': avg_rating
        })

        user = self.request.user
        context['has_reviewed'] = Review.objects.filter(book__pk=book_pk).filter(user=user).exists()
        return context

class EditReviewView(LoginRequiredMixin, UserIsCreatorMixin, UpdateView):
    model = Review
    form_class = EditReviewForm
    template_name = 'reviews/edit-review.html'
    pk_url_kwarg = 'review_pk'

    def get_object(self, queryset=None):
        book_pk = self.kwargs.get('book_pk')
        review_pk = self.kwargs.get('review_pk')
        return get_object_or_404(Review, pk=review_pk, book__pk=book_pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('reviews-list', kwargs={'book_pk': self.object.book.pk})

@login_required
def delete_review(request, book_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk, book__pk=book_pk)

    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    review.delete()
    return redirect(reverse('reviews-list', kwargs={'book_pk': book_pk}))