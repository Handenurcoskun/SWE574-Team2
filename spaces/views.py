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
from .models import Space, SpaceMembership, PrivateSpaceRequest
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
        results = PrivateSpaceRequest.objects.filter(space=viewed_space.id).all()
        if self.request.user in viewed_space.members.all():
            is_member = True
        else:
            is_member = False
        is_pending = False
        for result in results:
            if result.user == self.request.user:
                is_pending = True
        context["is_member"] = is_member
        context['posts'] = Post.objects.filter(space=viewed_space).order_by('-date_posted')
        context['private_space_requests'] = PrivateSpaceRequest.objects.filter(space=viewed_space.id)
        context["is_pending"] = is_pending
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
        if request.POST.get('space_id'):
            space = get_object_or_404(Space, id=request.POST.get('space_id'))
            if space.members.filter(id=request.user.id).exists():
                space.members.remove(request.user.id)
            else:
                if space.policy == 'public':
                    space.members.add(request.user.id)
                else:
                    psr = PrivateSpaceRequest()
                    psr.user = request.user
                    psr.space = space
                    psr.save()
        else:
            space = get_object_or_404(Space, id=pk)
            if request.POST.get("approved"):
                space.members.add(request.POST.get("approved"))
                PrivateSpaceRequest.objects.get(user_id=request.POST.get("approved")).delete()
            elif request.POST.get("declined"):
                PrivateSpaceRequest.objects.get(user_id=request.POST.get("declined")).delete()
    return HttpResponseRedirect(reverse('space-detail', args=[str(pk)]))
