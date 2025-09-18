from django.urls import path, re_path
from game.views.myspace.userlist import UserList
from game.views.myspace.getinfo import GetInfo
from game.views.myspace.post_view import PostView
from game.views.myspace.follow import FollowView
from game.views.myspace.player import PlayerView
from game.views.myspace.index import index


urlpatterns = [
    path('userlist/', UserList.as_view(), name="myspace_playerlist"),
    path('getinfo/', GetInfo.as_view(), name="myspace_getinfo"),
    path('post/', PostView.as_view(), name="myspace_post"),
    path('follow/', FollowView.as_view(), name="myspace_follow"),
    path('user/', PlayerView.as_view(), name="myspace_user"),
    re_path(r".*", index, name="myspace_index"),
]

