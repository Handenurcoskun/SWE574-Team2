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
from django.views import View

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import SpaceMembership



def home(request):
    context = {
        'spaces': Space.objects.all()
    }
    return render(request, 'spaces/space_list.html', context)

class SpaceListView(ListView):
    model = Space
    template_name = 'spaces/space_list.html'
    context_object_name = 'spaces'
    ordering = ['-date_created']

class SpaceDetailView(LoginRequiredMixin, DetailView):
    model = Space

    def get_filtered_posts(self):
        viewed_space = get_object_or_404(Space, id=self.kwargs['pk'])

        if self.request.user.is_authenticated:
            return Post.objects.filter(space=viewed_space).filter(
                Q(policy=Post.PUBLIC) | (Q(policy=Post.PRIVATE) & Q(author=self.request.user))
            ).order_by('-date_posted')
        return Post.objects.filter(space=viewed_space, policy=Post.PUBLIC).order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        viewed_space = get_object_or_404(Space, id=self.kwargs['pk'])

        if self.request.user in viewed_space.members.all():
            is_member = True
        else:
            is_member = False

        context["is_member"] = is_member
        context['posts'] = self.get_filtered_posts()
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

# spaces/views.py
class MembersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = SpaceMembership
    context_object_name = 'memberships'
    template_name = 'spaces/space_members.html'

    def get_queryset(self):
        space = get_object_or_404(Space, id=self.kwargs['pk'])
        memberships = SpaceMembership.objects.filter(space=space).exclude(user=space.owner).select_related('user')

        # Get or create an owner_membership for the owner and add it to the list of memberships
        owner_membership, _ = SpaceMembership.objects.get_or_create(user=space.owner, space=space,
                                                                    defaults={'role': 'owner'})
        memberships_with_owner = [owner_membership] + list(memberships)

        return memberships_with_owner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        space = self.get_space()
        context['user_membership'] = get_object_or_404(SpaceMembership, user=self.request.user, space=space)
        return context

    def test_func(self):
        space = self.get_space()
        if self.request.user == space.owner:
            return True

        membership = SpaceMembership.objects.filter(user=self.request.user, space=space).first()
        if membership:
            return True

        return False

    def get_space(self):
        return get_object_or_404(Space, id=self.kwargs['pk'])




class ChangeMemberRoleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        membership = get_object_or_404(SpaceMembership, id=self.kwargs['membership_id'])
        new_role = request.POST.get('new_role')
        user_membership = get_object_or_404(SpaceMembership, space=membership.space, user=self.request.user)

        # Don't allow the space owner's role to be changed
        if membership.role == 'owner' and new_role != 'owner':
            return redirect('members-list', membership.space.id)

        # Only allow the space owner and moderators to change member roles
        if membership.space.owner == request.user or (
                user_membership.is_moderator() and membership.role not in ['owner', 'moderator']):
            membership.role = new_role
            membership.save()

        # Allow pro members to change only basic member roles
        if user_membership.is_pro_member() and membership.role == 'basic_member':
            if new_role == 'pro_member':
                membership.role = new_role
                membership.save()
            else:
                return redirect('members-list', membership.space.id)

        return redirect('members-list', membership.space.id)

    def test_func(self):
        membership = get_object_or_404(SpaceMembership, id=self.kwargs['membership_id'])
        space = membership.space
        user_membership = get_object_or_404(SpaceMembership, space=space, user=self.request.user)

        # Only allow space owner, moderators and pro members to access this view
        if (space.owner == self.request.user) or \
                (user_membership.is_moderator() and membership.role not in ['owner', 'moderator']) or \
                (user_membership.is_pro_member() and membership.role == 'basic_member'):
            return True

        # Explicitly prevent basic members from accessing this view
        if user_membership.is_basic_member():
            return False

        return False


def search(request):
    query = request.GET.get('q')
    if query:
        spaces = Space.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

        # Filter out private posts
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query),
            policy='public'  # assuming 'public' represents a public post
        ).distinct()
    else:
        spaces = Post.objects.none()
        posts = Post.objects.none()

    context = {
        'spaces': spaces,
        'posts': posts,
    }
    return render(request, 'spaces/search.html', context)






