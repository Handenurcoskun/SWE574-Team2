from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View

from blog.models import Post
from spaces.models import Space
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic import ListView, DetailView
from .models import Profile, Category
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

def follow_unfollow_profile(request):
    if request.method == 'POST':
        my_profile = Profile.objects.get(user=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)
        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
    return redirect('profiles:profile-list')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            selected_categories = form.cleaned_data.get('categories')
            user.profile.categories.set(selected_categories)
            user.profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

class ProfileListView(ListView):
    model = Profile
    template_name = 'users/user_list.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/user_detail.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False
        context["follow"] = follow
        return context

def recommendation_view(request):
    # Kullanıcının seçtiği kategorileri al
    user = request.user
    profile = Profile.objects.get(user=user)
    selected_categories = profile.categories.all()

    # Bu kategorilere ait ve belirli kriterlere uyan spaceleri bul
    recommended_spaces = Space.objects.filter(
        category__in=selected_categories,
        posts__policy=Post.PUBLIC,
    ).annotate(
        post_count=Count('posts'),
        avg_likes=Avg('posts__likes')
    ).filter(
        post_count__gte=5,
        avg_likes__gte=3,
    )

    # Bu spaceleri bir öneri sayfasında göster
    return render(request, 'recommendations.html', {'spaces': recommended_spaces})