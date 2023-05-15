from django.urls import path
from .views import ProfileListView, ProfileDetailView, follow_unfollow_profile
from . import views

app_name = 'profiles'



urlpatterns = [
    path('list/', ProfileListView.as_view(), name='profile-list'),
    path('switch_follow/', follow_unfollow_profile, name='follow-unfollow'),
    path('list/<pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('recommendations/', views.recommendation_view, name='recommendations'),
]

