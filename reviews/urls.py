from django.urls import path, include

from reviews.forms import CreateReviewForm
from reviews.views import CreateReviewView

urlpatterns = [
    path('review/', include([
        path('add-review/', CreateReviewView.as_view(), name='add-review'),
    ]))
]