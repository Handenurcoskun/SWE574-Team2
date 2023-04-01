from django.urls import path
from .views import (
    SpaceListView,
    SpaceDetailView,
    SpaceCreateView,
    SpaceUpdateView,
    SpaceDeleteView,
    JoinSpaceView
)
from . import views

urlpatterns = [
    path('', SpaceListView.as_view(), name='spaces-home'),
    path('<int:pk>/', SpaceDetailView.as_view(), name='space-detail'),
    path('<int:pk>', JoinSpaceView, name='join-space'),
    path('new/', SpaceCreateView.as_view(), name='space-create'),
    path('<int:pk>/update', SpaceUpdateView.as_view(), name='space-update'),
    path('<int:pk>/delete', SpaceDeleteView.as_view(), name='space-delete'),
]
