from django.conf.urls.defaults import *

urlpatterns = patterns('game.views',
    url(r'^$','game_home',name='game_home'),
    url(r'^challenges/(?P<page_number>\d*)$','list_challenges',name='list_challenges'),
    url(r'^challenge/(?P<query>\d+)$','view_challenge',name='view_challenge'),
    url(r'^mysubmissions/(?P<page_number>\d*)$','list_submissions',name='list_submissions'),
    url(r'^submitfile/(?P<query>\d+)/$','submit_file',name='submit_file'),
    url(r'^submitkey/(?P<query>\d+)/$','submit_key',name='submit_key'),
    url(r'^submission/(?P<query>\d+)$','view_submission'),
    url(r'^unlockseries/?$','unlock_series', name='unlock_series'),
)
