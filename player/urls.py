from django.conf.urls.defaults import *

urlpatterns = patterns('player.views',
    url(r'^team/(?P<query>\d+)$','view_team_info',name='team_info'),
    url(r'^player/(?P<query>\d+)$','view_player_info',name='player_info'),
    url(r'^home/$','player_home',name='player_home'),
    url(r'^newplayer/$','register_new_player',name='new_player'),
    url(r'^confirmplayer/(?P<query>\d+)$','confirm_player',name='confirm_player'),
    url(r'^newteam/$','register_new_team',name='new_team'),
    url(r'^jointeam/$','join_team',name='join_team'),
    url(r'^leaveteam/$','leave_team',name='leave_team'),
    url(r'^requestban/$','request_ban',name='request_ban'),
    url(r'^updateteaminfo/$','update_team_info',name='update_team_info'),
    url(r'^updateplayerinfo/$','update_player_info',name='update_player_info'),
)
