from django import forms

from posts.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

        labels = {
            'title': 'Title:',
            'content': 'Content:',
            'author': 'Author:',

        }

        widgets = {
            'title':forms.TextInput(attrs={}),
            'content': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
            'author': forms.TextInput(attrs={}),
            'image1': forms.ClearableFileInput(attrs={'id': 'custom-upload','class': 'no-border', 'style': 'border: none;'}),
        }