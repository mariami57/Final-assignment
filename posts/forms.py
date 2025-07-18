from django import forms


from books.models import Book
from destinations.models import Destination
from posts.models import Post


class PostBaseForm(forms.ModelForm):
    book_choice = forms.ChoiceField(label='Choose a book', required=False)
    destination_choice = forms.ChoiceField(label='Choose a destination', required=False)
    class Meta:
        model = Post
        fields = ['title', 'book_choice', 'destination_choice', 'content','image1', 'image2', 'image3']
        labels = {
            'title': 'Title:',
            'content': 'Content:',
            'image1': 'First Image:',
            'image2': 'Second Image:',
            'image3': 'Third Image:',

        }


        widgets = {
            'title':forms.TextInput(attrs={}),
            'content': forms.Textarea(attrs={'class': 'form-control','rows': 10,'placeholder': 'Write your thoughts here...',}),
            'image1': forms.ClearableFileInput(attrs={'id': 'custom-upload','class': 'no-border', 'style': 'border: none;'}),
            'image2': forms.ClearableFileInput(attrs={'id': 'custom-upload2', 'class': 'no-border', 'style': 'border: none;'}),
            'image3': forms.ClearableFileInput(attrs={'id': 'custom-upload3', 'class': 'no-border', 'style': 'border: none;'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        books = Book.objects.all().values_list('id', 'title')
        self.fields['book_choice'].choices = [('', '--- Select a book ---')] + list(books)


        destinations = Destination.objects.all().values_list('id', 'name')
        self.fields['destination_choice'].choices = [('', '--- Select a destination ---')] + list(destinations)




    def clean(self):
        cleaned_data = super().clean()
        book_choice = cleaned_data.get('book_choice')

        dest_choice = cleaned_data.get('destination_choice')

        if not book_choice or not dest_choice:
            raise forms.ValidationError("Please select both book and destination at the same time.")

        return cleaned_data


class PostCreateForm(PostBaseForm):
    pass

class PostEditForm(PostBaseForm):
    pass

