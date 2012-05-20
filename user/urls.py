from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Login view (Django bulit-in)              
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'login.html'}),
    
    # Logout view  (Django bulit-in)
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    
    # User index page
    url(r'^$', 'user.views.index'),
    
    url(r'^config/$', 'user.views.config'),

)