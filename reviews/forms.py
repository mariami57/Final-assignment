from django import forms

from books.models import Book
from reviews.models import Review


class BaseReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')

        if self.user and book:
            already_reviewed = Review.objects.filter(user=self.user, book=book).exists()
            if already_reviewed:
                raise forms.ValidationError('You have already submitted a review for this book.')

        return cleaned_data

class CreateReviewForm(BaseReviewForm):
    pass

class EditReviewForm(BaseReviewForm):
    pass
