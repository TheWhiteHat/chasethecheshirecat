from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',include('inform.urls')),
    url(r'page/',include('inform.urls')),
    url(r'^players/',include('player.urls')),
    url(r'^game/', include('game.urls')),
    url(r'^score/',include('score.urls')),
    url(r'^admin/', include(admin.site.urls)),  
    url(r'^comments/', include('django.contrib.comments.urls')),  
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'Login.html'},name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'template_name': 'Logout.html'}, name='logout'),
    # Examples:
    # url(r'^$', 'chasethecheshirecat.views.home', name='home'),
    # url(r'^chasethecheshirecat/', include('chasethecheshirecat.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
