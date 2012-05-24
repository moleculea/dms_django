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
            return redirect_back(request,'page')
            
        # Non-VIP
        nonvip = request.GET.get('nonvip', None)
        if nonvip:
            updateInviteeStatus(user_id,nonvip,False)
            return redirect_back(request,'page')
            
        # Remove invitee
        remove = request.GET.get('remove', None)
        if remove:
            deleteUserInvitee(user_id,remove)
            return redirect_back(request,'page')
        

    user_list = getUserInvitee(user_id)
    user_list = pagination_creator(request, user_list,5)
    
    context = {'username':username,'user_list':user_list,'request':request}
    return render_to_response('meeting/meeting_scheduling_invitee.html',context,context_instance=RequestContext(request))

"""
scheduling_invitee_add()
# url: /meeting/msa/invitee/add/
""" 
def scheduling_invitee_add(request):
    
    username = request.user.username
    user_id = request.user.id

    if request.GET:
        invitee_id = request.GET.get('add', None)
        # If exists, insert it into dms.user_invitee for user_id (host)
        if invitee_id:
            saveUserInvitee(user_id,invitee_id)
            return redirect_back(request,'page')
            
    user_list = User.objects.exclude(id=user_id)
    user_invitee = getUserInviteeIDList(user_id)
    user_list = pagination_creator(request, user_list, 5)
    context = {'username':username,'user_list':user_list,'user_invitee':user_invitee,'request':request}
    return render_to_response('meeting/meeting_scheduling_invitee_add.html',context,context_instance=RequestContext(request))


"""
scheduling_config()
# url: /meeting/msa/config/

First step of meeting config: Day Range

""" 
def scheduling_config(request):
    username = request.user.username
    user_id = request.user.id
    import calendar,datetime
    from agenda.views import prevMonth,nextMonth
    agenda = calendar.Calendar(6)
    
    # Default render this month
    year = datetime.date.today().year
    month = datetime.date.today().month
    year_month = None
    
    
    if request.GET:
        # Get date from GET (?month=)
        year_month = request.GET.get('month', None)
        if year_month:
            year = int(year_month[:4])
            month = int(year_month[4:])
    
        # Add days
        add = request.GET.get('add', None)
        if add:
            # Check if unfinished config exists
            # If exists, add by updating existing day range
            if getUnfinishedConfig(user_id):
                meeting = getUnfinishedConfig(user_id)
                meeting_id = meeting.meeting_id
                # add is day (string)
                addDayRange(add,user_id,meeting_id)
            # If not exits, add by insert a new meeting
            else:
                addDayRange(add,user_id)
                
            return redirect_back(request,'month')
        
        # Remove days
        remove = request.GET.get('remove', None)
        if remove:
            # Unfinished meeting config must exist
            meeting = getUnfinishedConfig(user_id)
            meeting_id = meeting.meeting_id
            # remove is day (string)
            removeDayRange(remove,meeting_id)
            return redirect_back(request,'month')

    # Requested date
    date = datetime.date(year,month,1)
    monthsdays = agenda.monthdays2calendar(year,month)
    
    prev = prevMonth(date)
    next = nextMonth(date)
    
    # Get already selected days if exists
    selected_day = []
    if getUnfinishedConfig(user_id):
        meeting = getUnfinishedConfig(user_id)
        # Get the selected day
        selected_day = parseDayRange(meeting.day_range)

    # Generate month table
    htmltb = ""
    htmltb += "<table class=\"agendatable\"><tr>\n"
    htmltb += "<th>SUN</th><th>MON</th><th>TUE</th><th>WED</th><th>THU</th><th>FRI</th><th>SAT</th>"
    htmltb += "</tr>\n"
    for weeklist in monthsdays:
        htmltb +=  "<tr>"
        for datetuple in weeklist:
            day = datetuple[0]
            weekday = datetuple[1] # 0 is Monday, 6 is Sunday
            if day == 0:
                htmltb += "<td>&nbsp;</td>"
            else:
                # Days before today
                if datetime.date(year,month,day) < datetime.date.today():
                    htmltb += "<td><span class='agenda_invalid'>%s</span></td>"%(day)
                
                # Already selected days
                elif "%s%02d%02d"%(year,month,day) in selected_day:
                    if "?month" in request.get_full_path():
                        htmltb += "<td><a href='%s&remove=%s%s%s'><span class='agenda_notempty'>%s</span></a></td>"%(request.get_full_path(),year,str(month).zfill(2),str(day).zfill(2),day)
                    else:
                        htmltb += "<td><a href='?remove=%s%s%s'><span class='agenda_notempty'>%s</span></a></td>"%(year,str(month).zfill(2),str(day).zfill(2),day)
                
                # Today (not selected)
                elif datetime.date(year,month,day) == datetime.date.today():
                    if "?month" in request.get_full_path():
                        htmltb += "<td><a href='%s&add=%s%s%s'><span class='agenda_today'>%s</span></a></td>"%(request.get_full_path(),year,str(month).zfill(2),str(day).zfill(2),day)
                    else:
                        htmltb += "<td><a href='?add=%s%s%s'><span class='agenda_today'>%s</span></a></td>"%(year,str(month).zfill(2),str(day).zfill(2),day)

                # Weekend date (not selected)
                elif weekday == 5 or weekday ==6:
                    if "?month" in request.get_full_path():
                        htmltb += "<td><a href='%s&add=%s%s%s'><span class='agenda_weekend'>%s</span></a></td>"%(request.get_full_path(),year,str(month).zfill(2),str(day).zfill(2),day)
                    else:
                        htmltb += "<td><a href='?add=%s%s%s'><span class='agenda_weekend'>%s</span></a></td>"%(year,str(month).zfill(2),str(day).zfill(2),day)
                    
                # Normal date (not selected)
                else:
                    if "?month" in request.get_full_path():
                        htmltb += "<td><a href='%s&add=%s%s%s'><span class='agenda_day'>%s</span></a></td>"%(request.get_full_path(),year,str(month).zfill(2),str(day).zfill(2),day)
                    else:
                        htmltb += "<td><a href='?add=%s%s%s'><span class='agenda_day'>%s</span></a></td>"%(year,str(month).zfill(2),str(day).zfill(2),day)
                    
        htmltb += "</tr>"
        
    htmltb += "</table>\n"    
    
    
    context = {'username':username,'request':request,'htmltb':htmltb,'date':date,'prev':prev,'next':next}
    return render_to_response('meeting/meeting_scheduling_config.html',context,context_instance=RequestContext(request))

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

"""
redirect_back()

Redirect back to page-based perspective, avoiding multiple query string

"""

def redirect_back(request, getname):
    getvalue = request.GET.get(getname, None)
    if getvalue:
        return HttpResponseRedirect(request.path +"?%s=%s"%(getname,getvalue))
    else:
        return HttpResponseRedirect(request.path)