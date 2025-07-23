from django.urls import path, include

from reviews.forms import CreateReviewForm
from reviews.views import CreateReviewView, ReviewsPerBookView

urlpatterns = [
    path('book/<int:book_pk>/', include([
        path('reviews/', ReviewsPerBookView.as_view(), name='reviews-list'),
        path('add-review/', CreateReviewView.as_view(), name='add-review'),

    ]))
]