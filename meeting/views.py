# -*- coding: utf-8 -*-
# HTTP
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

# Template
from django.template import RequestContext

# login_required decorator
from django.contrib.auth.decorators import login_required

# Models
from meeting.models import *
from user.models import getUserInviteeIDList,saveUserInvitee,getUserInvitee,updateInviteeStatus,deleteUserInvitee

# Pagination
from django.core.paginator import Paginator

"""
index()
# url: /meeting/

"""

@login_required
def index(request):
    username = request.user.username
    meeting_list = getMeetingSuccessList()
    
    meeting_list = pagination_creator(request, meeting_list, 10)

    context = {'meeting_list': meeting_list,'username':username}

    return render_to_response('meeting/meeting.html',context,context_instance=RequestContext(request))


"""
meeting_canceled()
# url: /meeting/canceled/

"""

@login_required
def meeting_canceled(request):
    username = request.user.username
    meeting_list = getMeetingCanceledList()
    meeting_list = pagination_creator(request, meeting_list, 10)
    context = {'meeting_list': meeting_list,'username':username}
    return render_to_response('meeting/meeting_canceled.html',context,context_instance=RequestContext(request))


"""
meeting_success()
# url: /meeting/success/
# List of all successful meetings

"""

@login_required
def meeting_success(request):
    username = request.user.username
    meeting_list = getAllMeetingSuccessList()
    meeting_list = pagination_creator(request, meeting_list, 10)
    context = {'meeting_list': meeting_list,'username':username}
    return render_to_response('meeting/meeting_success.html',context,context_instance=RequestContext(request))
    
  
"""
scheduling_index()
# url: /meeting/msa/
""" 
def scheduling_index(request):
    username = request.user.username
    context = {'username':username}

    return render_to_response('meeting/meeting_scheduling.html',context,context_instance=RequestContext(request))
  

"""
participation_index()
# url: /meeting/ca/
""" 
def participation_index(request):
    username = request.user.username
    context = {'username':username}

    return render_to_response('meeting/meeting_participation.html',context,context_instance=RequestContext(request))
  
  
"""
scheduling_invitee()
# url: /meeting/msa/invitee/
""" 
def scheduling_invitee(request):
    
    username = request.user.username
    user_id = request.user.id
    
    if request.GET:
        # Status update
        # VIP
        vip = request.GET.get('vip', None)
        if vip:
            updateInviteeStatus(user_id,vip,True)
            
        # Non-VIP
        nonvip = request.GET.get('nonvip', None)
        if nonvip:
            updateInviteeStatus(user_id,nonvip,False)
            
        # Remove invitee
        remove = request.GET.get('remove', None)
        if remove:
            deleteUserInvitee(user_id,remove)
        
    user_list = getUserInvitee(user_id)
    user_list = pagination_creator(request, user_list,5)
    
    context = {'username':username,'user_list':user_list,'request':request}
    return render_to_response('meeting/meeting_scheduling_invitee.html',context,context_instance=RequestContext(request))

"""
scheduling_invitee_config()
# url: /meeting/msa/invitee/config/
""" 
def scheduling_invitee_config(request):
    
    username = request.user.username
    user_id = request.user.id

    if request.GET:
        invitee_id = request.GET.get('add', None)
        # If exists, insert it into dms.user_invitee for user_id (host)
        if invitee_id:
            saveUserInvitee(user_id,invitee_id)

    user_list = User.objects.exclude(id=user_id)
    user_invitee = getUserInviteeIDList(user_id)
    user_list = pagination_creator(request, user_list, 5)
    context = {'username':username,'user_list':user_list,'user_invitee':user_invitee,'request':request}
    return render_to_response('meeting/meeting_scheduling_invitee_config.html',context,context_instance=RequestContext(request))



"""
View functions
"""
"""
pagination_creator()
Create Paginator instance with given request, data instance (e.g. QuerySet instance) and number of objects per page

Return the data instance

"""

def pagination_creator(request, instance, num_per_page):
    paginator = Paginator(instance, num_per_page)
    
    if request.GET:
        page = request.GET.get('page',1)
    else:
        page = 1

    instance = paginator.page(page)
    #except PageNotAnInteger:
        #instance = paginator.page(1)
    #except EmptyPage:
        #instance = paginator.page(paginator.num_pages)         
    return instance
