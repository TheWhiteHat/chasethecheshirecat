from django.conf.urls.defaults import *

urlpatterns = patterns('score.views',
    url(r'^$','score',name='score'),
)