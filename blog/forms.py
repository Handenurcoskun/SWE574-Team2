from django import forms
from django.forms import Textarea
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'rows': 3, 'cols': 40}),
        }


class PostCreateUnderSpaceForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'link', 'tags', 'policy', 'image']