from django import forms
from django.forms import Textarea
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'rows': 3, 'cols': 40}),
        }
