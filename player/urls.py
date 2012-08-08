from django.conf.urls.defaults import *

urlpatterns = patterns('player.views',
    url(r'^team/(?P<query>\d+)$','view_team_info'),
    url(r'^player/(?P<query>\d+)$','view_player_info'),
    url(r'^newplayer/$','register_new_player'),
    url(r'^newteam/$','register_new_team'),
)
