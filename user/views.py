# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.template import RequestContext
from django.template.loader import get_template


from user.models import UserSPADE, UserConfig
from django.contrib.auth.models import User
# login_required decorator
from django.contrib.auth.decorators import login_required
# Form
from django import forms
# Built-in forms
from django.contrib.auth.forms import PasswordChangeForm

"""
index()

# url: /user/
# Index page when a user login

"""
@login_required
def index(request):
    username = request.user.username
    #html = "Hello %s, welcome to the Distributed Meeting Scheduler"%username
    #return HttpResponse(html)
    return render_to_response('user.html',{'username':username})



"""
password()

# url: /user/password/
# Page for user to change password

"""
@login_required
def password(request):
    user = request.user
    if request.method == 'POST': # If the form has been submitted
        form = PasswordChangeForm(user, request.POST) # A form bound to the POST data
        if form.is_valid(): 
            # Call PasswordChangeForm.save() to save new password into User
            form.save()
            return HttpResponseRedirect('/user/') # Redirect after POST
    else:
        form = PasswordChangeForm(user)

    c = RequestContext(request, {'form': form})
    t = get_template('user_password.html')
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
    c = RequestContext(request, {'msa': data.msa_id,'ca':data.ca_id,'agenda':agenda})
    t = get_template('user_config.html')
    return HttpResponse(t.render(c))

