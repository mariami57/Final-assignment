from django import forms


from books.models import Book
from destinations.models import Destination
from posts.models import Post


class PostBaseForm(forms.ModelForm):
    book_choice = forms.CharField(label='Book', required=False)
    book_title = forms.CharField(label='Book Title', required=False)

    destination_choice = forms.CharField(label='Destination', required=False)
    destination_name = forms.CharField(label='Destination Name', required=False)


    class Meta:
        model = Post
        fields = ['title', 'book_choice', 'book_title','destination_choice', 'destination_name', 'content','image1', 'image2', 'image3']
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
        self.fields['book_choice'].choices = [('', '--- Select a book ---')] + list(books) + [("other", "Other")]


        destinations = Destination.objects.all().values_list('id', 'name')
        self.fields['destination_choice'].choices = [('', '--- Select a destination ---')] + list(destinations) + [("other", "Other")]

        if self.data:
            self.fields['book_choice'].initial = self.data.get('book_choice')
            self.fields['book_title'].initial = self.data.get('book_title')

            self.fields['destination_choice'].initial = self.data.get('destination_choice')
            self.fields['destination_name'].initial = self.data.get('destination_name')



    def clean(self):
        cleaned_data = super().clean()
        book_choice = cleaned_data.get('book_choice')
        book_title = cleaned_data.get('book_title')

        dest_choice = cleaned_data.get('destination_choice')
        dest_name = cleaned_data.get('destination_name')

        if (not book_choice and not book_title) or (not dest_choice and not dest_name):
            raise forms.ValidationError("Please select both book and destination.")

        return cleaned_data


class PostCreateForm(PostBaseForm):
    pass

class PostEditForm(PostBaseForm):
    pass

