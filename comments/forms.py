from django import forms

from comments.models import Comment


class CommentBaseForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={
            'rows': 3,
            'cols': 40,
            'placeholder': 'Write your comment...',
        })}

class CommentCreateForm(CommentBaseForm):
    pass

class CommentEditForm(CommentBaseForm):
    pass

class CommentDeleteForm(CommentBaseForm):
    pass
