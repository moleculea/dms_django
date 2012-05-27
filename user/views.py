# -*- coding: utf-8 -*-
# HTTP
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

# Template
from django.template import RequestContext
from django.template.loader import get_template

# Models
from django.contrib.auth.models import User
from user.models import *
from agenda.models import getUserConfig
from meeting.models import Meeting, UserInviteeMeeting

# login_required decorator
from django.contrib.auth.decorators import login_required

# Forms
from django import forms
from django.contrib.auth.forms import PasswordChangeForm

# Others
from django.core.urlresolvers import reverse

import django.contrib.auth.views as auth_views
from dms.public import pagination_creator,redirect_back

# Pagination
from django.core.paginator import Paginator

"""
login()

# url: /user/login/
# Login a user: if the user already login, redirect to /user/

"""

def login(request):
    import django.contrib.auth.views as auth_views
    # If the user already login
    if request.user.is_authenticated():
        return HttpResponseRedirect("/user/")
    
    # Render login form
    else:
        return auth_views.login(request, template_name="user/user_login.html")
        
    
"""
index()

# url: /user/
# Index page when a user login

"""
@login_required
def index(request, id=None):
    # id is captured from URL for external query page
    query = True

    if id:
        # Query id
        id = id
        query = False
    else:
        # Id in cookie
        id = request.user.id

    # Query User model
    data = User.objects.get(pk=id)
    
    username = data.username
    joined = data.date_joined
    group = data.is_superuser

    
    if group:
        group = "Administrator"
        
    else:
        group = "User"
        
    schedule = Meeting.objects.filter(host_id=id)
    schedule = len(schedule)
    
    invite = UserInviteeMeeting.objects.filter(invitee_id=id)
    invite = len(invite)
    
    context = {'username':username,'id':id,'joined':joined,'group':group,'query':query,'schedule':schedule,'invite':invite}
    return render_to_response('user/user.html',context,context_instance=RequestContext(request))


"""
password()

# url: /user/password/
# Page for user to change password

"""
@login_required
def password(request):
    user = request.user
    username = request.user.username
    if request.method == 'POST': # If the form has been submitted
        form = PasswordChangeForm(user, request.POST) # A form bound to the POST data
        if form.is_valid(): 
            # Call PasswordChangeForm.save() to save new password into User
            form.save()
            return HttpResponseRedirect('/user/') # Redirect after POST
    else:
        form = PasswordChangeForm(user)

    c = RequestContext(request, {'form': form,'username':username})
    t = get_template('user/user_password.html')
    return HttpResponse(t.render(c))


"""
config()

# url: /user/config/
# Configuration page for users

"""

@login_required
def config(request):

    username = request.user.username
    id = request.user.id
    user_config = getUserConfig(user_id=id)
    user_invitee = getUserInvitee(host_id=id)
    
    pref_period = None
    best_period = None
    ca = None
    
    
    if user_config.pref_period and user_config.pref_period != 65535:
        pref_period= user_config.pref_period
        
    if user_config.best_period and user_config.best_period != 65535:
        best_period= user_config.best_period
    """
    if user_config.msa_id:
        msa = user_config.msa_id
    """  
    if user_config.ca_id:
        ca = user_config.ca_id
        
    agenda = {'pref':pref_period,'best':best_period}
    
    c = RequestContext(request, {'ca': ca,'agenda':agenda,'username':username,'user_invitee':user_invitee})
    t = get_template('user/user_config.html')
    return HttpResponse(t.render(c))


"""
list()

# url: /user/list/
# Page for listing all users

"""

@login_required
def list(request):
    username = request.user.username
    data = User.objects.all()
    
    data = pagination_creator(request, data, 10)
    
    """
    if request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data = paginator.page(paginator.num_pages)
    
    """
    return render_to_response('user/user_list.html',{'data':data,'username':username}, context_instance=RequestContext(request))


"""
message()

# url: /user/message/
"""

@login_required
def message(request):
    username = request.user.username
    user_id = request.user.id
    
    if request.GET:
        message = request.GET.get('message', None)
        if message:
            readMessage(message)
            return redirect_back(request,'page')
        
    message = getUserMessage(user_id)
    message = pagination_creator(request, message, 10)
    
    context = {'message':message,'username':username,'request':request}
    
    return render_to_response('user/user_message.html',context, context_instance=RequestContext(request))


