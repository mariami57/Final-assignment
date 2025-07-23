from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from books.models import Book
from reviews.forms import CreateReviewForm
from reviews.models import Review


# Create your views here.
class CreateReviewView(CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = 'reviews/add-review.html'
    success_url = reverse_lazy('posts')

    def dispatch(self, request, *args, **kwargs):
        self.book_id = request.GET.get('book_id')
        self.book = None
        if self.book_id:
            self.book = get_object_or_404(Book, pk=self.book_id)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if self.book:
            initial['book'] = self.book
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['book'].queryset = Book.objects.all()

        if self.book:
            form.fields['book'].initial = self.book
            form.fields['book'].disabled = True
        return form

    def form_valid(self, form):
        book_id = self.request.GET.get('book_id')
        if self.book:
            form.instance.book = self.book
        return super().form_valid(form)
