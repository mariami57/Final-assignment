from django import forms

from books.models import Book
from reviews.models import Review


class BaseReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user', 'book' )


class CreateReviewForm(BaseReviewForm):
    pass

class EditReviewForm(BaseReviewForm):
    pass
