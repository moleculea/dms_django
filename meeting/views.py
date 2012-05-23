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

"""
index()
# url: /meeting/

"""

@login_required
def index(request):
    meeting_list = getMeetingSuccessList()
    meeting = Meeting.objects.all()
    context = {'meeting_list': meeting_list}

    return render_to_response('meeting/meeting.html',context,context_instance=RequestContext(request))

