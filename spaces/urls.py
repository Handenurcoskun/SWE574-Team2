from django.urls import path
from .views import (
    SpaceListView,
    SpaceDetailView,
    SpaceCreateView,
    SpaceUpdateView,
    SpaceDeleteView,
    JoinSpaceView,
    MembersListView,
    ChangeMemberRoleView,
    search,
    user_posts,
    recommend_spaces,
)
# below are paths
urlpatterns = [
    path('', SpaceListView.as_view(), name='spaces-home'),
    path('<int:pk>/', SpaceDetailView.as_view(), name='space-detail'),
    path('<int:pk>/join', JoinSpaceView, name='join-space'),
    path('new/', SpaceCreateView.as_view(), name='space-create'),
    path('<int:pk>/update/', SpaceUpdateView.as_view(), name='space-update'),
    path('<int:pk>/delete/', SpaceDeleteView.as_view(), name='space-delete'),
    path('spaces/<int:pk>/members/', MembersListView.as_view(), name='members-list'),
    path('spaces/memberships/<int:membership_id>/change_member_role/', ChangeMemberRoleView.as_view(), name='change-member-role'),
    path('search/', search, name='search'),
    path('user/<str:username>/', user_posts, name='user_posts'),
    path('recommendations/', recommend_spaces, name='recommendations'),
]
