"""
URLconf
meeting/

"""
from django.conf.urls import patterns, include, url

urlpatterns = patterns('meeting.views',
    # Index (success meetings to be held after today)
    url(r'^$','index'),
    
    # Canceled meetings
    url(r'^canceled/$','meeting_canceled'),
        
    # All successful meetings
    url(r'^success/$','meeting_success'),
    
    # Scheduling (MSA Index)
    url(r'^msa/$','scheduling_index'),
    
    # Scheduling invitee
    url(r'^msa/invitee/$','scheduling_invitee'),   
     
    # Scheduling invitee add (add invitee from user list)
    url(r'^msa/invitee/add/$','scheduling_invitee_add'),    

    # Scheduling config (First step: day range)
    url(r'^msa/config/$','scheduling_config'),    
    
    # Participation (CA Index)
    url(r'^ca/$','participation_index'),
    
    
)