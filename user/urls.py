"""
URLconf
user/

    * login
    * logout
    * /
    * password
    * config
    * list
    * message
    
"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Login view            
    url(r'^login/$', 'user.views.login'),
    
    # Logout view  (Django bulit-in)
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    
    # User index page (internal)
    url(r'^$', 'user.views.index', name="internal"),
    
    # User page (external query)
    url(r'^id=(?P<id>\d+)/$', 'user.views.index', name="external"),
    
    # User password change page
    url(r'^password/$', 'user.views.password'),
    
    # User configuration page
    url(r'^config/$', 'user.views.config'),
    
    # User list page
    url(r'^list/$', 'user.views.list'),
    

)