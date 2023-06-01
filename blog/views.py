from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views import View
from blog.wikidata import search_wikidata_entities

from users.models import Profile
from spaces.models import Space, SpaceMembership
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from itertools import chain
from django.db.models import Q
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from . import models
from .models import Post
from .forms import CommentForm, PostCreateUnderSpaceForm

from .models import WikidataEntity


def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "blog/home.html", context)


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(policy=Post.PUBLIC)
                | (Q(policy=Post.PRIVATE) & Q(author=self.request.user))
            ).order_by("-date_posted")
        return Post.objects.filter(policy=Post.PUBLIC).order_by("-date_posted")


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user, policy=Post.PUBLIC).order_by(
            "-date_posted"
        )


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        viewed_post = get_object_or_404(Post, id=self.kwargs["pk"])
        if viewed_post.favourites.filter(id=self.request.user.id).exists():
            save = True
        else:
            save = False
        context["save"] = save
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.get_object()
            comment.user = request.user
            comment.save()
            return redirect("post-detail", pk=self.get_object().pk)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post

    fields = ["title", "content", "link", "tags", "policy", "image"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostCreateUnderSpaceView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateUnderSpaceForm

    def get_space(self):
        space_id = self.kwargs.get("space_id")
        space = get_object_or_404(Space, id=space_id)
        return space

    def dispatch(self, request, *args, **kwargs):
        space = self.get_space()
        user_membership = SpaceMembership.objects.filter(
            user=request.user, space=space
        ).first()
        user_existence = False

        if (
            SpaceMembership.objects.filter(user=request.user, space=space).exists()
            or request.user == space.owner
        ):
            user_existence = True

        if not user_existence:
            raise PermissionDenied(
                "You must be a member of this space to create a post."
            )

        if request.user != space.owner:
            if (
                space.policy == Space.PRIVATE
                and user_membership.role == SpaceMembership.BASIC_MEMBER
            ):
                raise PermissionDenied(
                    "You must be a Pro Member or Moderator in a private space to create a post."
                )

        return super().dispatch(request, *args, **kwargs)

    def check_duplicate_link(self, form):
        link = form.cleaned_data.get("link")
        space = self.get_space()

        duplicate_post = Post.objects.filter(space=space, link=link).first()
        if duplicate_post:
            context = self.get_context_data()
            context["duplicate_post"] = duplicate_post
            context["form"] = form
            return self.render_to_response(context)
        return None

    def form_valid(self, form):
        if "deny" in self.request.POST:
            return HttpResponseRedirect(reverse("blog-home"))
        if "confirm" not in self.request.POST:
            duplicate_response = self.check_duplicate_link(form)
            if duplicate_response:
                return duplicate_response

        form.instance.author = self.request.user
        form.instance.space = self.get_space()
        post = form.save()

        wikitags = form.cleaned_data["wikitags"].split(",")
        for tag in wikitags:
            tag = tag.strip()
            if tag:  # avoid empty tags
                try:
                    entity = WikidataEntity.objects.get(label=tag)
                    post.wikitags.add(entity)
                except WikidataEntity.DoesNotExist:
                    # Handle the case when the tag does not exist in the database
                    messages.error(self.request, f"Tag {tag} does not exist.")

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateUnderSpaceForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()

        post.wikitags.clear()

        wikitags = form.cleaned_data["wikitags"].split(",")
        for tag in wikitags:
            tag = tag.strip()
            if tag:  # avoid empty tags
                try:
                    entity = WikidataEntity.objects.get(id=tag)
                    post.wikitags.add(entity)                    
                except WikidataEntity.DoesNotExist:
                    # Handle the case when the tag does not exist in the database
                    messages.error(self.request, f"Tag {tag} does not exist.")
        post.save()
        
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})


def get_title(html):
    """Scrape page title."""
    title = None
    if html.title.string:
        title = html.title.string
    elif html.find("meta", property="og:title"):
        title = html.find("meta", property="og:title").get("content")
    elif html.find("meta", property="twitter:title"):
        title = html.find("meta", property="twitter:title").get("content")
    elif html.find("h1"):
        title = html.find("h1").string
    return title


def get_description(html):
    """Scrape page description."""
    description = None
    if html.find("meta", property="description"):
        description = html.find("meta", property="description").get("content")
    elif html.find("meta", property="og:description"):
        description = html.find("meta", property="og:description").get("content")
    elif html.find("meta", property="twitter:description"):
        description = html.find("meta", property="twitter:description").get("content")
    elif html.find("p"):
        description = html.find("p").contents
    return description


def get_image(html):
    """Scrape share image."""
    image = None
    if html.find("meta", property="image"):
        image = html.find("meta", property="image").get("content")
    elif html.find("meta", property="og:image"):
        image = html.find("meta", property="og:image").get("content")
    elif html.find("meta", property="twitter:image"):
        image = html.find("meta", property="twitter:image").get("content")
    elif html.find("img", src=True):
        image = html.find_all("img").get("src")
    return image


def generate_preview(request):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Max-Age": "3600",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    }

    url = request.GET.get("link")
    print(url)
    req = requests.get(url, headers)
    html = BeautifulSoup(req.content, "html.parser")
    meta_data = {
        "title": get_title(html),
        "description": get_description(html),
        "image": get_image(html),
    }

    print(meta_data)

    return JsonResponse(meta_data)


def posts_of_following_profiles(request):
    profile = Profile.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    posts = []
    paginate_by = 5
    qs = None
    for u in users:
        p = Post.objects.filter(author=u, policy=Post.PUBLIC)
        posts.append(p)
    my_posts = Post.objects.filter(author=request.user)
    posts.append(my_posts)
    if len(posts) > 0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)
    return render(request, "blog/myspace.html", {"posts": qs})


def FavouritesView(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, id=request.POST.get("post_id"))
        if post.favourites.filter(id=request.user.id).exists():
            post.favourites.remove(request.user.id)
        else:
            post.favourites.add(request.user.id)
    return HttpResponseRedirect(reverse("post-detail", args=[str(pk)]))


def favourite_posts(request):
    context = {"favourites": Post.objects.filter(favourites=request.user)}
    print(context)
    return render(request, "blog/favourites.html", context)


def filter_tags(request, pk):
    context = {"taggedposts": Post.objects.filter(tags=pk)}
    return render(request, "blog/filtertags.html", context)


# blog/views.py
class ModeratePostsListView(LoginRequiredMixin, ListView):
    ...

    def get_queryset(self):
        space = get_object_or_404(Space, id=self.kwargs["pk"])
        return Post.objects.filter(space=space, status=Post.PENDING).order_by(
            "-date_posted"
        )


class PostModerationActionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = self.kwargs["pk"]
        action = request.POST.get("action")

        post = get_object_or_404(Post, id=post_id)
        space_membership = SpaceMembership.objects.filter(
            space=post.space, user=request.user
        ).first()

        # Check if the user is the space owner or has the 'moderator' role
        if not (
            request.user == post.space.owner
            or (space_membership and space_membership.role == SpaceMembership.MODERATOR)
        ):
            # Redirect the user to an error page or show a message indicating insufficient permissions
            # Replace 'error-page' with the appropriate URL
            return HttpResponseRedirect(reverse("error-page"))

        if action == "approve":
            post.status = Post.APPROVED
        elif action == "reject":
            post.status = Post.REJECTED
        elif action == "remove":
            post.status = Post.REMOVED

        post.save()

        # Redirect the user back to the list of posts pending moderation
        # Replace 'moderate-posts-list' with the URL of the ModeratePostsListView
        return HttpResponseRedirect(
            reverse("moderate-posts-list", args=[post.space.id])
        )


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post_id = request.POST.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        response_data = {
            "post_id": post_id,
            "likes_count": post.likes.count(),
            "liked": liked,
        }
        return JsonResponse(response_data)


class WikidataEntityAutocompleteView(View):
    def get_queryset(self, query):
        if not query:
            return []

        # Try to get entities from the database
        entities_db = WikidataEntity.objects.filter(label__icontains=query)
        if entities_db.exists():
            return [
                {
                    "id": entity.entity_id,
                    "label": entity.label,
                    "description": entity.description,
                }
                for entity in entities_db
            ]

        # If no entity was found in the database, query the API
        entities_api = search_wikidata_entities(query)

        # Save the entities found through the API in the database
        for entity in entities_api:
            if not WikidataEntity.objects.filter(entity_id=entity["id"]).exists():
                WikidataEntity.objects.create(
                    entity_id=entity["id"],
                    label=entity["label"],
                    description=entity["description"],
                )

        return [
            {
                "id": entity["id"],
                "label": entity["label"],
                "description": entity["description"],
            }
            for entity in entities_api
        ]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("term", "")
        queryset = self.get_queryset(query)
        return JsonResponse(queryset, safe=False)


# class WikidataSubtypeAutocompleteView(View):
#     def get_queryset(self, query):
#         if not query:
#             return []

#         subtypes = WikidataSubtype.objects.filter(label__icontains=query)
#         return [
#             {"id": subtype.subtype_id, "label": subtype.label} for subtype in subtypes
#         ]

#     def get(self, request, *args, **kwargs):
#         query = request.GET.get("term", "")
#         queryset = self.get_queryset(query)
#         return JsonResponse(queryset, safe=False)
