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
        memberships = SpaceMembership.objects.filter(space=space).exclude(user=space.owner)

        # Include the owner as an 'owner' role membership
        owner_membership = SpaceMembership(user=space.owner, space=space, role='owner')
        owner_membership.id = -1  # Assign a temporary ID for the owner's membership
        memberships_with_owner = [owner_membership] + list(memberships)

        return memberships_with_owner

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
        membership_id = self.kwargs['membership_id']
        membership = get_object_or_404(SpaceMembership, id=membership_id)
        new_role = request.POST.get('new_role')

        if new_role == 'owner':
            # Transfer ownership
            space = membership.space
            space.owner = membership.user
            space.save()

            # Change the old owner's role to a moderator
            old_owner_membership = get_object_or_404(SpaceMembership, space=space, user=request.user)
            old_owner_membership.role = 'moderator'
            old_owner_membership.save()

        else:
            # Update the member's role
            membership.role = new_role
            membership.save()

        return redirect('members-list', membership.space.id)

    def test_func(self):
        membership_id = self.kwargs['membership_id']
        membership = get_object_or_404(SpaceMembership, id=membership_id)
        return self.request.user == membership.space.owner






# spaces/views.py
class ModeratePostView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        space = post.space
        membership = get_object_or_404(SpaceMembership, space=space, user=self.request.user)
        return membership.is_moderator()

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        post = get_object_or_404(Post, id=self.kwargs['post_id'])

        if action == 'approve':
            post.is_approved = True
        elif action == 'reject':
            post.is_approved = False
        elif action == 'remove':
            post.delete()
            return HttpResponseRedirect(reverse('space-detail', args=[str(post.space.pk)]))

        post.save()
        return HttpResponseRedirect(reverse('space-detail', args=[str(post.space.pk)]))
