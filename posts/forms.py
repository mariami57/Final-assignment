from django import forms


from books.models import Book
from destinations.models import Destination
from posts.mixins import BookDestinationHandlerMixin
from posts.models import Post
from posts.validators import OtherDestinationFormatValidator


class PostBaseForm(forms.ModelForm):
    book_choice = forms.ChoiceField(
        label='Book', required=False,
        widget=forms.Select(attrs={'class': 'select-search'})
    )
    book_title = forms.CharField(label='Book Title', required=False)

    destination_choice = forms.ChoiceField(
        label='Destination', required=False,
        widget=forms.Select(attrs={'class': 'select-search'})
    )
    destination_name = forms.CharField(
        label='Destination Name',
        help_text='Please fill in the following format: destination name, country',
        required=False,
    )

    class Meta:
        model = Post
        fields = ['title', 'book_choice', 'book_title', 'destination_choice', 'destination_name',
                  'content', 'image1', 'image2', 'image3']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        books = Book.objects.all().values_list('id', 'title')
        self.fields['book_choice'].choices = [('', '--- Select a book ---')] + \
                                             [(str(bid), title) for bid, title in books] + \
                                             [('other', 'Other')]

        destinations = Destination.objects.all().values_list('id', 'name')
        self.fields['destination_choice'].choices = [('', '--- Select a destination ---')] + \
                                                    [(str(did), name) for did, name in destinations] + \
                                                    [('other', 'Other')]


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
            raise forms.ValidationError('Please select both a book and a destination.')

        if dest_choice == 'other':
            if dest_name:
                if ',' not in dest_name or len(dest_name.split(', ')) != 2:
                    self.add_error(
                        'destination_name',
                        'Destination must be in the format "Destination name, Country".'
                    )
            else:
                self.add_error(
                    'destination_name',
                    'Please provide a destination in the format "Destination name, Country".'
                )
        else:
            cleaned_data['destination_name'] = ''

        return cleaned_data


class PostCreateForm(PostBaseForm):
    pass

class PostEditForm(BookDestinationHandlerMixin, PostBaseForm):
   class Meta(PostBaseForm.Meta):
       fields = ['title', 'book_choice', 'destination_choice', 'content', 'image1',
                 'image2', 'image3']

   def __init__(self, *args, **kwargs):
       instance = kwargs.get('instance')
       self.request = kwargs.pop('request', None)
       super().__init__(*args, **kwargs)

       if instance:
           if instance.book:
               self.fields['book_choice'].initial = str(instance.book.id)
           if instance.destination:
               self.fields['destination_choice'].initial = str(instance.destination.id)

   def save(self, commit=True):
       post = super().save(commit=False)


       if hasattr(self, 'request'):
           book, destination = self.handle_book_and_destination(self)
           print("BOOK:", book)
           print("DEST:", destination)
           post.book = book
           post.destination = destination

       if commit:
           post.save()

       return post