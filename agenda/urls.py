"""
URLconf
agenda/


"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns('agenda.views',
    # Index
    url(r'^$','index'),
    # Year view
    url(r'^(?P<year>\d{4})/$','year_view'),
    # Month view
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$','month_view'),
    # Day view
    #url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$','day_view'),
)