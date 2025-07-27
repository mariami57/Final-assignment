from django import forms


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

        existing_review = Review.objects.filter(book=book, user=self.user)

        if self.instance.pk:
            existing_review = existing_review.exclude(pk=self.instance.pk)

        if existing_review.exists():
                raise forms.ValidationError('You have already submitted a review for this book.')

        return cleaned_data

class CreateReviewForm(BaseReviewForm):
    pass

class EditReviewForm(BaseReviewForm):
    pass
