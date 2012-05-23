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
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$','day_view',name='show'),
    
    # Day view (update daily_period)
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<action>[^/=]+)=(?P<period>\d{1,2})/$','day_view',name='update'),
    
    # Day view (update best_period and pref_period)
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<type>[^/]+)/(?P<action>[^/=]+)=(?P<period>\d{1,2})/$','day_view', name='type'),
    
    # Event
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/event/$','event_view',name='event'),

    # Config
    url(r'^config/(?P<type>[^/]+)/(?P<action>[^/=]+)=(?P<period>\d{1,2})/$','config'),
    

    # Config (update best_period and pref_period)
    url(r'^config/$','config'),
)