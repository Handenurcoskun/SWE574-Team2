from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from users.models import Profile
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from itertools import chain
from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Space, SpaceMembership
from blog.models import Post

def home(request):
    context = {
        'spaces': Space.objects.all()
    }
    return render(request, 'space/spaces.html', context)

class SpaceListView(ListView):
    model = Space
    template_name = 'space/spaces.html'
    context_object_name = 'spaces'
    ordering = ['-date_created']

class SpaceDetailView(LoginRequiredMixin, DetailView):
    model = Space
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        viewed_space = get_object_or_404(Space, id=self.kwargs['pk'])
        if self.request.user in viewed_space.members.all():
            is_member = True
        else:
            is_member = False
        context["is_member"] = is_member
        context['posts'] = Post.objects.filter(space=viewed_space).order_by('-date_posted')
        return context

class SpaceCreateView(LoginRequiredMixin, CreateView):
    model = Space
    fields = ['name', 'description', 'policy', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class SpaceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Space
    fields = ['name', 'description', 'policy', 'image']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        space = self.get_object()
        if self.request.user == space.owner:
            return True
        return False

class SpaceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Space
    success_url = '/'

    def test_func(self):
        space = self.get_object()
        if self.request.user == space.owner:
            return True
        return False

def JoinSpaceView(request, pk):
    if request.method == 'POST':
        space = get_object_or_404(Space, id=request.POST.get('space_id'))
        if space.members.filter(id=request.user.id).exists():
            space.members.remove(request.user.id)
        else:
            space.members.add(request.user.id)
    return HttpResponseRedirect(reverse('space-detail', args=[str(pk)]))


def display_posts(request):
    public_posts = Post.objects.filter(private=False)
    user_posts = Post.objects.filter(user=request.user)
    posts = public_posts | user_posts
    return render(request, 'display_posts.html', {'posts': posts})