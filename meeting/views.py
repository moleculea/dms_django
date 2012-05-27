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
from user.models import getUserInviteeIDList,saveUserInvitee,getUserInvitee,updateInviteeStatus,deleteUserInvitee, getUserInviteeVIP,UserConfig

# Paginator
from dms.public import pagination_creator,redirect_back

from dms.public import dailyPeriod2list


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
@login_required
def scheduling_index(request):
    username = request.user.username
    user_id = request.user.id
    
    meeting = Meeting.objects.filter(host_id=user_id)
    meeting_success = getMeetingSuccess(user_id)
    meeting_canceled = MeetingCanceled.objects.filter(host_id=user_id)
    meeting_failed = getMeetingFailed(user_id)
    
    meeting = len(meeting)
    meeting_success = len(meeting_success)
    meeting_canceled = len(meeting_canceled)
    meeting_failed = len(meeting_failed)
    
    invitee = getUserInvitee(user_id)
    invitee_vip = getUserInviteeVIP(user_id)
    
    invitee = len(invitee)
    invitee_vip = len(invitee_vip)
    invitee_nonvip = invitee - invitee_vip
    
    context = {'username':username,'meeting_success':meeting_success,'meeting_canceled':meeting_canceled,'meeting_failed':meeting_failed,'meeting':meeting,'invitee':invitee,'invitee_vip':invitee_vip,'invitee_nonvip':invitee_nonvip}
    
    return render_to_response('meeting/meeting_scheduling.html',context,context_instance=RequestContext(request))
  

"""
participation_index()
# url: /meeting/ca/
""" 
@login_required
def participation_index(request):
    
    username = request.user.username
    user_id = request.user.id

    if request.GET:
        # Status update
        # VIP
        accept = request.GET.get('accept', None)
        meeting = request.GET.get('meeting', None)
        if accept and meeting:
            updateUIM(user_id,meeting,accept)
            return HttpResponseRedirect("/meeting/ca/")
        
    user_ca = getUserCA(user_id)
    uim = getInvitation(user_id)
    uim = pagination_creator(request, uim, 10)

    context = {'username':username,'uim':uim,'user_ca':user_ca}

    return render_to_response('meeting/meeting_participation.html',context,context_instance=RequestContext(request))
  



"""
participation_config()
# url: /meeting/ca/
""" 
@login_required
def participation_config(request):
    username = request.user.username
    user_id = request.user.id
    if request.method == 'POST':
        
        form = ParticipationConfigForm(request.POST)
        
        if form.is_valid():
            accept = form.cleaned_data['accept']
            participate = form.cleaned_data['participate']
            
            user_ca = getUserCA(user_id)
            
            # if user_id exists in dms.user_ca
            if user_ca:
                # Update
                user_ca.accept = accept
                user_config = UserConfig.objects.get(user_id=user_id)
                user_config.ca_id = user_ca
                user_ca.save()
                user_config.save()
                
            else:
                # Insert
                user_spade = UserSPADE.objects.get(user_id=user_id)
                user_ca = UserCA(user_id=user_spade,active='True',accept=accept)
                user_config = UserConfig.objects.get(user_id=user_id)
                user_config.ca_id = user_ca
                user_ca.save()
                user_config.save()
            
            # Do nothing (default state: CA is running in SPADE) 
            if participate == "1":
                user_ca = getUserCA(user_id)
                user_ca.active = 'True'
                user_ca.save()
                        
            else:
                user_ca = getUserCA(user_id)
                if user_ca:
                    # Add to CA for ALCC
                    addToCA(user_id, 'False')
                    # Update user_ca.active to False
                    user_ca.active = 'False'
                    user_ca.save()
                
                
        return HttpResponseRedirect("/meeting/ca/")
    
    
    else:

        #config_form = ParticipationConfigForm()
        user_ca = getUserCA(user_id)
    
        context = {'username':username,'user_ca':user_ca}
    
        return render_to_response('meeting/meeting_participation_config.html',context,context_instance=RequestContext(request))
      

"""
participation_invitation()

# url: /meeting/ca/invitation/?meeting=ID

"""
@login_required
def participation_invitation(request):
    
    username = request.user.username
    user_id = request.user.id
    meeting_id = 0
    if request.GET:
        # Status update
        # VIP
        accept = request.GET.get('accept', None)
        meeting_id = request.GET.get('id', None)
        if accept and meeting_id:
            updateUIM(user_id,meeting_id,accept)
            return redirect_back(request,'id')

    user_ca = getUserCA(user_id)
    uim = getInvitationMeeting(user_id,meeting_id)
    success = MeetingSuccess.objects.filter(meeting_id=meeting_id)

    context = {'username':username,'user_ca':user_ca,'uim':uim,'success':success}

    return render_to_response('meeting/meeting_participation_invitation.html',context,context_instance=RequestContext(request))
  
    
  
"""
scheduling_invitee()
# url: /meeting/msa/invitee/
""" 
@login_required
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
    user_list = pagination_creator(request, user_list,10)
    
    context = {'username':username,'user_list':user_list,'request':request}
    return render_to_response('meeting/meeting_scheduling_invitee.html',context,context_instance=RequestContext(request))


"""
scheduling_invitee_add()
# url: /meeting/msa/invitee/add/
""" 
@login_required
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
    user_list = pagination_creator(request, user_list, 10)
    context = {'username':username,'user_list':user_list,'user_invitee':user_invitee,'request':request}
    return render_to_response('meeting/meeting_scheduling_invitee_add.html',context,context_instance=RequestContext(request))


"""
scheduling_config()
# url: /meeting/msa/config/

First step of meeting config: Day Range

""" 
@login_required
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
    day_range_message = None
    
    if getCurrentMeeting(user_id):
        return HttpResponseRedirect("/meeting/msa/ms/")
    
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
        
        # Day range message
        day_range_message = request.GET.get('day_range', None)
        if day_range_message == "0":
            day_range_message = "Please select at least one day."
        else:
            day_range_message = None
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
        
    # Format selected days into datetime.date instance
    format_selected_day = formatDateList(selected_day)
    
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
    
    
    context = {'username':username,'request':request,'htmltb':htmltb,'date':date,'prev':prev,'next':next,'day_range_message':day_range_message,'format_selected_day':format_selected_day}
    return render_to_response('meeting/meeting_scheduling_config.html',context,context_instance=RequestContext(request))




"""
scheduling_config_pref()
# url: /meeting/msa/config/pref/

Second step of meeting config: Preference Period

""" 
@login_required
def scheduling_config_pref(request):
    
    username = request.user.username
    user_id = request.user.id 
    meeting_id = 0
    pref_period = 0
    pref_message = None
    
    # Avoid direct get to the page
    if getUnfinishedConfig(user_id):
        
        meeting = getUnfinishedConfig(user_id)
        if meeting.day_range:
            
            meeting_id = meeting.meeting_id
            
        else:
            # Redirect back
            return HttpResponseRedirect('/meeting/msa/config/?day_range=0')  
    else:
        # Redirect back
        return HttpResponseRedirect('/meeting/msa/config/?day_range=0')
    
    # Update pref_period
   
    if request.GET:
        subperiod = request.GET.get('select', None)
        if subperiod:
            subperiod = int(subperiod)
            changePrefPeriod(meeting_id, 'select', subperiod)
        
        subperiod = request.GET.get('cancel', None)
        if subperiod:
            subperiod = int(subperiod)
            changePrefPeriod(meeting_id, 'cancel', subperiod)  
    
        # Preference Period message
        pref_message = request.GET.get('pref', None)
        if pref_message == "0":
            pref_message = "Please select at least one hour."
        else:
            pref_message = None
    
    # Reload meeting instance      
    meeting = getUnfinishedConfig(user_id)
    pref_period = meeting.pref   
    
    pref_period = dailyPeriod2list(pref_period)
    time = [str(i).zfill(2) for i in range(6,23)]
    context = {'username':username,'pref_period':pref_period,'time':time,'pref_message':pref_message}
    return render_to_response('meeting/meeting_scheduling_config_pref.html',context,context_instance=RequestContext(request))


"""
scheduling_config_init()
# url: /meeting/msa/config/init/

Final step of meeting config: (Other) Initial parameters

""" 
@login_required
def scheduling_config_init(request):   
    
    username = request.user.username
    user_id = request.user.id 
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == "Start":
            # Save the config and start scheduling
            # When saving, force meeting.length to 0 to indicate unfinished config
            # Get the meeting (meeting_id) that is submitted
            meeting = getUnfinishedConfig(user_id)
            meeting_id = meeting.meeting_id
            
            # Save the initial parameters as it was
            form = MeetingForm(request.POST, instance=meeting)
            form.save()
            
            # Add all active invitees( of the host, i.e. this user )
            # to dms.user_invitee_meeting
            addAllUIM(user_id, meeting_id)
            
            # Add to MSA so that ALCC will start MSA
            addToMSA(user_id, meeting_id, True)
            
            
            return HttpResponseRedirect("/meeting/msa/ms/?id=%s"%meeting_id)
            
        elif action == "Save":
            # Temporarily save initial parameters
            # Force save length as 0 to make it unfinished
            meeting = getUnfinishedConfig(user_id)
            
            form = MeetingForm(request.POST, instance=meeting)
            modform = form.save(commit=False)
            modform.length = 0
            modform.save()
        
            return HttpResponseRedirect("/meeting/msa/ms/")
            
    else:

        # Avoid direct get to the page
        if getUnfinishedConfig(user_id):
            meeting = getUnfinishedConfig(user_id)
            if meeting.day_range:
                meeting_id = meeting.meeting_id
            else:
                # Redirect back
                return HttpResponseRedirect('/meeting/msa/config/?day_range=0')  
        else:
            # Redirect back
            return HttpResponseRedirect('/meeting/msa/config/')
        
        # Get meeting instance 
        meeting = getUnfinishedConfig(user_id)
        # if meeting.search_bias is not empty, this means the user saved the config before
        # Thus, render the instance
        if meeting.search_bias:
            meeting_form = MeetingForm(instance=meeting)
            
        else:   
            meeting_form = MeetingForm(instance=meeting,initial={'search_bias': 'AVERAGE_IDLE','delimit':5})
            
        selected_day = parseDayRange(meeting.day_range)
        format_selected_day = formatDateList(selected_day)
        
        pref_period = meeting.pref
        pref_period_list = combinedPeriod2Time(pref_period)
        
        if not pref_period_list:
            # Redirect back
            return HttpResponseRedirect('/meeting/msa/config/pref/?pref=0')     
        
        #user_invitee = getUserInvitee(user_id)
        user_invitee = getActiveUserInvitee(user_id)
        
        context = {'username':username,'meeting_form':meeting_form,'format_selected_day':format_selected_day,'pref_period_list':pref_period_list,'user_invitee':user_invitee}
        return render_to_response('meeting/meeting_scheduling_config_init.html',context,context_instance=RequestContext(request))


"""

scheduling_management()
# url: /meeting/msa/ms/
# url: /meeting/msa/ms/?id=MEETING_ID
"""

@login_required
def scheduling_management(request):
    username = request.user.username
    user_id = request.user.id 
    
    meeting_id = None
    meeting_id = request.GET.get('id',None)
    

    # If meeting_id is passed from GET (?id=MEETING_ID)    
    # Render the management interface for this meeting 
    # This interface is able manage or view any meeting in dms.meeting
    if meeting_id:
        meeting_id= int(meeting_id)
        ### GET actions ###
        # Update conf_period with the chosen period
        choose = request.GET.get('choose', None)
        if choose != None:
            updateConfPeriod(meeting_id, choose)
            return HttpResponseRedirect('/meeting/msa/ms/?id=%s'%meeting_id)    

        invite = request.GET.get('invite', None)
        if invite:
            updateInvite(meeting_id, invite)
            return HttpResponseRedirect('/meeting/msa/ms/?id=%s'%meeting_id)  
        
        cancel = request.GET.get('cancel', None)
        if cancel:
            # Update meeting.cancel or force cancel
            updateCancel(meeting_id, user_id, cancel)
            return HttpResponseRedirect('/meeting/msa/ms/?id=%s'%meeting_id)
            
        
        cancel = request.GET.get('reschedule', None)
        if cancel:
            updateReschedule(meeting_id)
            return HttpResponseRedirect('/meeting/msa/ms/?id=%s'%meeting_id)
        
        ### Initialize variables for stage actions ###
        stage = 0
        choose_period = None
        invitation = None
        
        ### Stage actions ###
        stage = getStage(meeting_id, user_id)
        
        # Stage 1: Let the host choose period
        if stage == 1:
            choose_period = getChoosePeriod(meeting_id)

        if stage == 4:
            pass
        
        ### Load meeting and invitee instance ###
        # Get static things (initial parameters, other status, invitees) and display
        # Get the meeting
        meeting = Meeting.objects.get(host_id=user_id, meeting_id=meeting_id)
        
        #### Get the state of meeting (meeting_id GET from ?id=MEETING_ID) ###
        meeting_state = getMeetingState(meeting_id, user_id)
        
        # Get invitees of this meeting
        # If this is an unfinised meeting config, 
        # uim_invitee is an empty list
        
        #uim_invitee = getUIMInvitee(meeting_id)
        uim_invitee = getUIMWithStatus(meeting_id,user_id)
        meeting_state_text = ['Unfinished', 'Being scheduled', 'Succeeded', 'Expired', 'Canceled']
        context = {'username':username,'request':request,'meeting': meeting,'uim_invitee': uim_invitee,'stage':stage,'choose_period':choose_period,'meeting_state':meeting_state,'meeting_state_text':meeting_state_text} 
        
        return render_to_response('meeting/meeting_scheduling_management.html',context,context_instance=RequestContext(request))
        
    # If meeting_id is not given in GET
    # Render the general management interface
    else:
        # Render unfinished meeting config if exists
        unfinished_meeting = getUnfinishedConfig(user_id)
        
        # Render the current meeting being scheduled
        # before the meeting succeeded or is canceled
        current_meeting = getCurrentMeeting(user_id)
        
        context = {'username':username,'unfinished_meeting': unfinished_meeting, 'current_meeting': current_meeting} 
        
        return render_to_response('meeting/meeting_scheduling_management.html',context,context_instance=RequestContext(request))



@login_required
def scheduling_log(request):
    
    username = request.user.username
    user_id = request.user.id
    
    
    meeting = Meeting.objects.filter(host_id=user_id)
    meeting_list = []
    
    meeting_state_text = ['Unfinished', 'Being scheduled', 'Succeeded', 'Expired', 'Canceled']
    for mt in meeting:
        md = {}
        md['meeting_id'] = mt.meeting_id
        md['topic'] = mt.topic
        md['stage_code'] = getStage(mt.meeting_id, user_id)
        meeting_state = getMeetingState(mt.meeting_id, user_id)
        md['meeting_state'] = meeting_state_text[meeting_state]
        meeting_list.append(md)
        
    context = {'username':username,'meeting_list':meeting_list} 
    return render_to_response('meeting/meeting_scheduling_log.html',context,context_instance=RequestContext(request))


