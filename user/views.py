# -*- coding: utf-8 -*-
# HTTP
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

# Template
from django.template import RequestContext
from django.template.loader import get_template

# Models
from user.models import UserSPADE, UserConfig
from django.contrib.auth.models import User

# login_required decorator
from django.contrib.auth.decorators import login_required

# Forms
from django import forms
from django.contrib.auth.forms import PasswordChangeForm

# Others
from django.core.urlresolvers import reverse

import django.contrib.auth.views as auth_views

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
        
    schedule = 0
    invite = 0
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
    data = UserConfig.objects.get(pk=id)
    agenda = {'pref':data.pref_period,'best':data.best_period}
    c = RequestContext(request, {'msa': data.msa_id,'ca':data.ca_id,'agenda':agenda,'username':username})
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
    return render_to_response('user/user_list.html',{'data':data,'username':username}, context_instance=RequestContext(request))