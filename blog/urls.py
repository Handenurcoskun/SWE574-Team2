from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    FavouritesView,
    generate_preview,
    posts_of_following_profiles
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('myspace', posts_of_following_profiles, name='following-posts'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>', FavouritesView, name='post-favourites'),
    path('favouriteposts', views.favourite_posts, name='favourite-posts'),
    path('filtertags/<int:pk>', views.filter_tags, name='filter-tags'),
    path('searchkeyword/', views.search_keyword, name='search-keyword'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/preview', generate_preview, name='post-preview'),
    path('about/', views.about, name='blog-about'),
]
