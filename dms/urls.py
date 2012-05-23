"""
URLconf
    Root
    * agenda  ==> agenda.urls
    * user    ==> user.urls
    * meeting ==> meeting.urls
    
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # url(r'^web/', include('web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^agenda/',include('agenda.urls')),
    url(r'^user/',include('user.urls')),
    url(r'^meeting/',include('meeting.urls')),
)

urlpatterns += staticfiles_urlpatterns()