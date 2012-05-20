# -*- coding: utf-8 -*-
from django.http import HttpResponse
from user.models import UserSPADE, UserConfig
from django.contrib.auth.decorators import login_required

"""
index()

# url: /user/
# Index page when a user login

"""
@login_required
def index(request):
    username = request.user.username
    html = "Hello %s, welcome to the Distributed Meeting Scheduler"%username
    return HttpResponse(html)

@login_required
def config(request):
    #user = UserSPADE.objects.get(pk=1)
    #username = user.user_name
    username = request.user.username
    id = request.user.id
    html = "Hello World, " + username
    data = UserConfig.objects.get(pk=id)
    html += "\n%s %s %s %s"%(data.msa_id, data.ca_id, data.pref_period, data.best_period)
    return HttpResponse(html)


