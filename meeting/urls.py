"""
URLconf
meeting/

"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns('meeting.views',
    # Index
    url(r'^$','index'),
    
    # MSA Index
    # CA Index
)