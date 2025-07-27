from django.urls import path, include

from reviews.views import CreateReviewView, ReviewsPerBookView, EditReviewView, delete_review

urlpatterns = [
    path('review/', include([
        path('add/', CreateReviewView.as_view(), name='add-review'),

    ])),
    path('book/<int:book_pk>/', include([
        path('reviews/', ReviewsPerBookView.as_view(), name='reviews-list'),
        path('add-review/', CreateReviewView.as_view(), name='add-review'),

        path('<int:review_pk>/', include([
            path('edit/', EditReviewView.as_view(), name='edit-review'),
            path('delete/', delete_review, name='delete-review'),
        ])),

    ])),
]