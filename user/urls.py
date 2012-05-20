from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Login view (Django bulit-in)              
    url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'user_login.html'}),
    
    # Logout view  (Django bulit-in)
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login'),
    
    # User index page
    url(r'^$', 'user.views.index'),
    
    # User password change page
    url(r'^password/$', 'user.views.password'),
    
    url(r'^config/$', 'user.views.config'),
    


)