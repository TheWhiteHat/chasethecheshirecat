from django.conf.urls.defaults import *

urlpatterns = patterns('inform.views',
    url(r'^$','view_main_page'),
    url(r'^info/(?P<query>\w+)$','view_info_page',name='info_page'),
    url(r'^announcement/(?P<query>\w+)$','view_announcement'),
    url(r'^announcements/(?P<page_number>\d*)$','list_announcements'),
    url(r'^newinfopage/$','create_info_page'),
    url(r'^newannouncement/$','create_announcement'),
)
