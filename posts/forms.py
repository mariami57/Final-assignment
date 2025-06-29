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
            'image1': 'First Image:',
            'image2': 'Second Image:',
            'image3': 'Third Image:',

        }

        widgets = {
            'title':forms.TextInput(attrs={}),
            'content': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
            'author': forms.TextInput(attrs={}),
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