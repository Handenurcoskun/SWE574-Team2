from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import MultipleHiddenInput
from .models import Profile, Category


class UserUpdateForm(forms.ModelForm):
        email = forms.EmailField()

        class Meta:
            model = User
            fields = ['username', 'email']

# CATEGORIES = [
#     ('art', 'Art'),
#     ('baseball', 'Baseball'),
#     ('basketball', 'Basketball'),
#     ('business', 'Business'),
#     ('culture', 'Culture'),
#     ('economy', 'Economy'),
#     ('education', 'Education'),
#     ('entertainment', 'Entertainment'),
#     ('environment', 'Environment'),
#     ('earthquakes', 'Earthquakes'),
#     ('fashion', 'Fashion'),
#     ('food', 'Food'),
#     ('football', 'Football'),
#     ('games', 'Games'),
#     ('health', 'Health'),
#     ('history', 'History'),
#     ('hockey', 'Hockey'),
#     ('language', 'Language'),
#     ('literature', 'Literature'),
#     ('music', 'Music'),
#     ('nature', 'Nature'),
#     ('philosophy', 'Philosophy'),
#     ('politics', 'Politics'),
#     ('religion', 'Religion'),
#     ('science', 'Science'),
#     ('society', 'Society'),
#     ('software', 'Software'),
#     ('sports', 'Sports'),
#     ('technology', 'Technology'),
#     ('tennis', 'Tennis'),
#     ('travel', 'Travel'),
#     ('volleyball', 'Volleyball'),
# ]


class ProfileUpdateForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    custom_category = forms.CharField(
        max_length=100,
        required=False,
        help_text="Enter a new category name if you can't find it in the list above."
    )

    class Meta:
        model = Profile
        fields = ['image', 'categories', 'custom_category']

    def save(self, commit=True):
        profile = super(ProfileUpdateForm, self).save(commit=False)
        if commit:
            profile.save()
        selected_categories = self.cleaned_data.get('categories')
        custom_category_name = self.cleaned_data.get('custom_category')
        if custom_category_name:
            custom_category, created = Category.objects.get_or_create(name=custom_category_name)
            selected_categories = list(selected_categories) + [custom_category]
        profile.categories.set(selected_categories)
        return profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'categories']

    def clean(self):
        cleaned_data = super().clean()
        custom_categories = self.data.getlist('custom_categories')
        categories = cleaned_data.get('categories')
        if categories is None:
            categories = []
        else:
            categories = list(categories)

        for category_name in custom_categories:
            category, created = Category.objects.get_or_create(name=category_name)
            categories.append(category)
            cleaned_data['categories'] = categories
        return cleaned_data

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.save()
        categories = self.cleaned_data.get('categories')
        user.profile.categories.add(*categories)
        return user
