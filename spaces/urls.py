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
    ModeratePostView,
)

urlpatterns = [
    path('', SpaceListView.as_view(), name='spaces-home'),
    path('<int:pk>/', SpaceDetailView.as_view(), name='space-detail'),
    path('<int:pk>', JoinSpaceView, name='join-space'),
    path('new/', SpaceCreateView.as_view(), name='space-create'),
    path('<int:pk>/update', SpaceUpdateView.as_view(), name='space-update'),
    path('<int:pk>/delete', SpaceDeleteView.as_view(), name='space-delete'),
    path('spaces/<int:pk>/members/', MembersListView.as_view(), name='members-list'),
    path('spaces/<int:membership_id>/change_member_role/', ChangeMemberRoleView.as_view(), name='change-member-role'),
    path('spaces/<int:post_id>/moderate_post/', ModeratePostView.as_view(), name='moderate-post'),
]
