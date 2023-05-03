# spaces/forms.py
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Search'}))