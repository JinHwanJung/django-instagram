from django.urls import path

from account.views import ExploreUsers, FollowUser, UnFollowUser, Search, UserProfile, UserFollowers, UserFollowings, \
    ChangePassword

app_name = "account"

urlpatterns = [
    path('explore/', ExploreUsers.as_view(), name='explore_users'),
    path('<int:user_id>/follow/', FollowUser.as_view(), name='follow_user'),
    path('<int:user_id>/unfollow/', UnFollowUser.as_view(), name='unfollow_user'),
    path('search/', Search.as_view(), name='search_user'),
    path('<str:username>/', UserProfile.as_view(), name='user_profile'),
    path('<str:username>/followers/', UserFollowers.as_view(), name='user_followers'),
    path('<str:username>/followings/', UserFollowings.as_view(), name='user_followings'),
    path('<str:username>/password/', ChangePassword.as_view(), name='change_password')
]
