from django import forms


from books.models import Book
from destinations.models import Destination
from posts.models import Post



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
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'book_choice', 'book_title', 'destination_choice', 'destination_name',
                  'content', 'image1', 'image2', 'image3']
        # ... (widgets and labels stay the same)

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
            raise forms.ValidationError("Please select both book and destination.")

        return cleaned_data


class PostCreateForm(PostBaseForm):
    pass

class PostEditForm(PostBaseForm):
   class Meta(PostBaseForm.Meta):
       fields = ['title', 'book_choice', 'destination_choice', 'content', 'image1',
                 'image2', 'image3']

   def __init__(self, *args, **kwargs):
       instance = kwargs.get('instance')
       super().__init__(*args, **kwargs)

       if instance:
           if instance.book:
               self.fields['book_choice'].initial = str(instance.book.id)
           if instance.destination:
               self.fields['destination_choice'].initial = str(instance.destination.id)

   # def save(self, commit=True):
   #     post = super().save(commit=False)
   #
   #     book_id = self.cleaned_data.get('book_choice')
   #     if book_id:
   #         try:
   #             post.book = Book.objects.get(id=book_id)
   #         except Book.DoesNotExist:
   #             post.book = None
   #
   #     destination_id = self.cleaned_data.get('destination_choice')
   #     if destination_id:
   #         try:
   #             post.destination = Destination.objects.get(id=destination_id)
   #         except Destination.DoesNotExist:
   #             post.destination = None
   #
   #     if commit:
   #         post.save()
   #
   #     return post