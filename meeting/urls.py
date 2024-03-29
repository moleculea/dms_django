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
    
    # Scheduling config (Second step: preference period)
    url(r'^msa/config/pref/$','scheduling_config_pref'),  
    
    # Scheduling config (Final step: other initial parameters)
    url(r'^msa/config/init/$','scheduling_config_init'),  
    
    # Scheduling Management
    url(r'^msa/ms/$','scheduling_management'),      
    
    # Scheduling log
    url(r'^msa/log/$','scheduling_log'),      
        
    # Participation (CA Index)
    url(r'^ca/$','participation_index'),
    
    # Participation config
    url(r'^ca/config/$','participation_config'),
    
    # Participation invitation
    url(r'^ca/invitation/$','participation_invitation'),
    
)