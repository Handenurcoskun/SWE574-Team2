from django.urls import path
from .views import ProfileListView, ProfileDetailView, follow_unfollow_profile, recommend_users


app_name = 'profiles'



urlpatterns = [
    path('list/', ProfileListView.as_view(), name='profile-list'),
    path('switch_follow/', follow_unfollow_profile, name='follow-unfollow'),
    path('list/<pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('recommendations/', recommend_users, name='user-recommendations'),

]

