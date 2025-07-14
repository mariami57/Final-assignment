from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from reviews.forms import CreateReviewForm
from reviews.models import Review


# Create your views here.
class CreateReviewView(CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = 'reviews/add-review.html'
    success_url = reverse_lazy('posts')