from django import forms

from books.models import Book
from destinations.models import Destination
from posts.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        book = forms.ModelChoiceField(queryset=Book.objects.all())
        destination = forms.ModelChoiceField(queryset=Destination.objects.all())
        fields = ['title', 'book', 'destination', 'content','book_review', 'image1', 'image2', 'image3']

        labels = {
            'title': 'Title:',
            'book': 'Book:',
            'destination': 'Destination:',
            'content': 'Content:',
            'book_review': 'Book Review:',
            'image1': 'First Image:',
            'image2': 'Second Image:',
            'image3': 'Third Image:',

        }

        widgets = {
            'title':forms.TextInput(attrs={}),
            'content': forms.Textarea(attrs={'class': 'form-control','rows': 10,'placeholder': 'Write your thoughts here...',}),
            'book_review': forms.Textarea(attrs={'class': 'form-control','rows': 10,'placeholder': 'Write your review here...',}),
            'image1': forms.ClearableFileInput(attrs={'id': 'custom-upload','class': 'no-border', 'style': 'border: none;'}),
            'image2': forms.ClearableFileInput(attrs={'id': 'custom-upload2', 'class': 'no-border', 'style': 'border: none;'}),
            'image3': forms.ClearableFileInput(attrs={'id': 'custom-upload3', 'class': 'no-border', 'style': 'border: none;'}),
        }

class PostCreateForm(PostBaseForm):
    pass

class PostEditForm(PostBaseForm):
    pass

class PostDeleteForm(PostBaseForm):
    pass