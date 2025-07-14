from django import forms

from reviews.models import Review


class BaseReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']

class CreateReviewForm(BaseReviewForm):
    pass
