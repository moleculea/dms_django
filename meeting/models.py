from django.db import models
from django.contrib.auth.models import User
from user.models import UserSPADE, UserConfig, UserInvitee, getUserInvitee

from django import forms
from django.forms import ModelForm

import sys
sys.path.append('/home/anshichao/dms/spade/Algorithms')
from DIGIT import *

"""
UserMSA

# Model of dms.user_msa

"""

class UserMSA(models.Model):
    msa_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.UserSPADE', db_column="user_id", related_name='+')
    active = models.CharField(max_length=15) # True | False
    
    class Meta:
        db_table = u'user_msa'

"""
UserCA

# Model of dms.user_ca

"""

class UserCA(models.Model):
    ca_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.UserSPADE', db_column="user_id", related_name='+')
    active = models.CharField(max_length=15) # True | False
    accept = models.CharField(max_length=15,blank=True) # True (ACCEPT) | False (DECLINE) | NULL (SILENT)
    
    class Meta:
        db_table = u'user_ca'
  
 
"""
UserInviteeMeeting (UIM)

# Model of dms.user_invitee_meeting

"""   
class UserInviteeMeeting(models.Model):
    
    id = models.AutoField(primary_key=True)
    host_id = models.ForeignKey('user.UserSPADE', db_column="host_id", related_name='+')
    meeting_id = models.ForeignKey('Meeting', db_column="meeting_id", related_name='+')
    invitee_id = models.ForeignKey('user.UserSPADE', db_column="invitee_id", related_name='+')
    available = models.CharField(max_length=15)
    accept = models.CharField(max_length=15)
    class Meta:
        db_table = u'user_invitee_meeting'   
   

"""
Meeting

# Model of dms.meeting

"""
      
class Meeting(models.Model):
    meeting_id = models.AutoField(primary_key=True)
    host_id = models.ForeignKey('user.UserSPADE',db_column='host_id',related_name='+')
    
    # Initial parameters
    length = models.IntegerField()
    day_range = models.CharField(max_length=1500)
    pref = models.IntegerField()
    topic = models.CharField(max_length=1500)
    location = models.CharField(max_length=1500,blank=True)
    search_bias = models.CharField(max_length=60,blank=True)
    delimit = models.IntegerField(null=True,blank=True)
    conf_method = models.CharField(max_length=60)
    
    # Functional columns
    conf_period = models.CharField(max_length=60,blank=True) # True | False | NULL | Period
    choose_period = models.CharField(max_length=1500,blank=True)
    invite = models.CharField(max_length=60,blank=True) # True | False | NULL
    cancel = models.CharField(max_length=15,blank=True) # True | False | NULL
    reschedule = models.CharField(max_length=15,blank=True) # True | NULL
    stat_id = models.ForeignKey('MeetingStat',db_column="stat_id",related_name='+', null=True)
    
    class Meta:
        db_table = u'meeting'        

    # Convert Preference Period into time format list
    def preftotime(self):
        return combinedPeriod2Time(self.pref)
    
    # Convert Day Range's ";" into <br/>
    def breakdayrange(self):
        date_list = self.day_range.split(";")
        format_list = formatDateList(date_list)
        return format_list
    
    
"""
MeetingForm

Model form of Meeting
"""
class MeetingForm(ModelForm):
    LENGTH_CHOICES = (
        (1,'1 hour'),
        (2,'2 hours'),
        (3,'3 hours'),
        (4,'4 hours'), 
        (5,'5 hours'),  
    )
    
    SEARCH_BIAS_CHOICES = (
        ('AVERAGE_IDLE','Average idleness'),
        ('DAY_LENGTH','Day length'),
    )    
    
    DELIMIT_CHOICES = (
        (1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5'), (6,'6'), (7,'7'), (8,'8'),
    )  
    
    CONF_METHOD_CHOICES = (
        ('AUTO','Automatic'),
        ('PROMPT','Ask me'),
    )      
    
    length = forms.ChoiceField(choices=LENGTH_CHOICES)
    search_bias = forms.ChoiceField(choices=SEARCH_BIAS_CHOICES)
    delimit = forms.ChoiceField(choices=DELIMIT_CHOICES, widget=forms.Select(attrs={'class':'delimit_select'}))
    conf_method = forms.ChoiceField(choices=CONF_METHOD_CHOICES, widget=forms.Select(attrs={'class':'conf_method_select'}))
    
    class Meta:
        model = Meeting
        fields = ('topic', 'length', 'location','search_bias','delimit','conf_method')
        



"""
MeetingStat

# Model of dms.meeting_stat

"""
      
class MeetingStat(models.Model):
    stat_id = models.AutoField(primary_key=True)
    date = models.DateField()
    conf_period = models.IntegerField()
    confirm = models.IntegerField()
    decline = models.IntegerField()
    class Meta:
        db_table = u'meeting_stat'
        
    # Convert Preference Period into time format list
    def periodtotime(self):
        if self.conf_period:
            return period2Time(self.conf_period)
        else:
            return None
    
    
"""
MeetingCanceled

# Model of dms.meeting_canceled

"""
      
class MeetingCanceled(models.Model):
    id = models.AutoField(primary_key=True)
    meeting_id = models.ForeignKey('Meeting', unique=True, db_column='meeting_id',related_name='+')
    host_id = models.ForeignKey('user.UserSPADE',db_column='host_id',related_name='+')
    date = models.DateField()
    period = models.CharField(max_length=60) # NULL | False | Period 
    stage = models.CharField(max_length=24) # GEN | INVT | FB
    reason = models.CharField(max_length=765)
    class Meta:
        db_table = u'meeting_canceled'
        
    def period_time(self):
        if self.period.isdigit():
            
            time = period2Time(int(self.period))
            return time
        else:
            return None
        
"""
MeetingSuccess

# Model of dms.meeting_sucess

"""

class MeetingSuccess(models.Model):
    id = models.AutoField(primary_key=True)
    meeting_id = models.ForeignKey('Meeting', unique=True, db_column='meeting_id',related_name='+')
    host_id = models.ForeignKey('user.UserSPADE',db_column='host_id')
    date = models.DateField()
    period = models.IntegerField()
    
    class Meta:
        db_table = u'meeting_success'
        
    def period_time(self):
        if self.period:
            time = period2Time(self.period)
            return time
        else:
            return None
    
"""
MSA

# Model of dms.msa
# Temporary table for ALCC to control MSA agents

"""

class MSA(models.Model):
    id = models.AutoField(primary_key=True)
    meeting_id = models.ForeignKey('Meeting', unique=True, db_column='meeting_id',related_name='+')
    user_id = models.ForeignKey('user.UserSPADE', db_column='user_id',related_name='+')
    active = models.CharField(max_length=15)
    class Meta:
        db_table = u'msa'
        
"""
CA

# Model of dms.ca
# Temporary table for ALCC to control CA agents

"""        

class CA(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user.UserSPADE', db_column='user_id',related_name='+')
    active = models.CharField(max_length=15)
    class Meta:
        db_table = u'ca'


class ParticipationConfigForm(forms.Form):
    
    # Small bugs, not userd to render in HTML, but only to receive POST
    PARTICIPATE_CHOICES = ((1,'Yes'),(0,'No'))
    ACCEPT_CHOICES = (('True','Accept'),('False','Decline'),('','Silent'))
    
    participate = forms.ChoiceField(widget=forms.RadioSelect,choices=PARTICIPATE_CHOICES)
    accept = forms.ChoiceField(required=False,widget=forms.RadioSelect,choices=ACCEPT_CHOICES)

"""
Model functions

"""

"""
getMeetingSuccessList()
Get list of successful meetings that are not canceled (truly and temporarily successful)
i.e. meetings in dms.meeting_success and not in dms.meeting_canceled

Meeting dates before TODAY will be excluded from the results
"""
def getMeetingSuccessList():
    import datetime
    today = datetime.date.today()
    meeting_canceled = MeetingCanceled.objects.all().values('meeting_id').query
    meeting_list = MeetingSuccess.objects.exclude(meeting_id__in=meeting_canceled).filter(date__gt=today).order_by('date','id')
    return meeting_list


"""
getDueMeetingSuccessList()

Get list of successful meetings that are due

"""
def getDueMeetingSuccessList():
    import datetime
    today = datetime.date.today()
    meeting_canceled = MeetingCanceled.objects.all().values('meeting_id').query
    meeting_list = MeetingSuccess.objects.exclude(meeting_id__in=meeting_canceled).filter(date__lt=today).order_by('date','id')
    return meeting_list

"""
getAllMeetingSuccessList()

Get all successful meetings that are not canceled.
Including those dates before TODAY
"""

def getAllMeetingSuccessList():
    meeting_list = MeetingSuccess.objects.all()
    return meeting_list

"""
getMeetingCanceledList()

Get list of canceled meetings (dms.meeting_canceled)
"""
def getMeetingCanceledList():
    meeting_canceled = MeetingCanceled.objects.all()
    return meeting_canceled


"""
getUnfinishedConfig()

Get the unfinished meeting config (not yet submitted meeting, with only day range or preference period )

Check whether meeting length (dms.meeting.length) is zero to identify an unfinished config

Only ONE unfinished config of a single host is allowed to exist in dms.meeting

"""

def getUnfinishedConfig(user_id):
    # Check whether unfinished config exists
    check = Meeting.objects.filter(host_id=user_id,length=0)
    
    if len(check) > 0:
        meeting = Meeting.objects.get(host_id=user_id,length=0)
        
        # Return the meeting instance for update use
        return meeting
    # If not exist, return None which indicates insert use
    else:
        return None

"""
getCurrentMeeting()

Get the current meeting being scheduled (right after the start of scheduling and before it is successful or canceled)

"""

def getCurrentMeeting(user_id):
    
    success = MeetingSuccess.objects.all().values('meeting_id').query
    canceled = MeetingCanceled.objects.all().values('meeting_id').query
    
    # Meetings whose config has finished (length!=0) that are neither in dms.meeting_success nor dms.meeting_canceled
    # Normally only ONE or none
    
    current = Meeting.objects.filter(host_id=user_id).exclude(meeting_id__in=success).exclude(meeting_id__in=canceled).exclude(length=0)
    
    return current
    
    
"""
parseDayRange()
Parse a ";" separated string into a string list
"20120601;20120602;" => ['20120601','20120602']

"""

def parseDayRange(day_range):
    if day_range:
        dlist = day_range.split(';')
        return dlist
    else:
        return []

"""
addDayRange()
Add a day to day range
meeting_id = None: no unfinished meeting config, new config and add day to empty day range
"""    

def addDayRange(day,user_id,meeting_id=None):
    # day is a string
    # Unfinished config exists
    if meeting_id:
        meeting = Meeting.objects.get(meeting_id=meeting_id)
        # If meeting_id exists, get and parse the day first 
        day_range = parseDayRange(meeting.day_range)
        # Append the day
        day_range.append(day)
        # Join list to string
        day_range= ";".join(day_range)
        meeting.day_range = day_range
        # Update
        meeting.save()
    else:
        # Add this single, first day to day range
        # Other fields uses default values
        
        ##############################################
        
        # First time to insert default meeting values
        user = User.objects.get(id=user_id)
        user_spade = UserSPADE.objects.get(user_id=user)
        meeting = Meeting(host_id=user_spade, length=0, day_range=day, pref=0, topic="No topic")
        # Insert
        meeting.save()

"""
removeDayRange()
Remove a day from day range
"""    
    
def removeDayRange(day,meeting_id):
    
    meeting = Meeting.objects.get(meeting_id=meeting_id)
    # Get and parse day range
    day_range = parseDayRange(meeting.day_range)
    
    if day in day_range:
        # Remove the day
        day_range.remove(day)
        # Join the list into string
        day_range= ";".join(day_range)
        meeting.day_range = day_range
        # Update
        meeting.save()

"""
savePrefPeriod()

Update dms.meeting.pref_period
"""

def savePrefPeriod(meeting_id, pref_period):
    meeting = Meeting.objects.get(meeting_id=meeting_id)
    meeting.pref = pref_period
    meeting.save()
    

def getPrefPeriod(meeting_id):
    meeting = Meeting.objects.get(meeting_id=meeting_id)
    return meeting.pref


def changePrefPeriod(meeting_id, action, subperiod):
    pref_period = getPrefPeriod(meeting_id)
    id = None;
    # If select == True
    # Change 0 into 1
    if action == "cancel":
        pref_period = pref_period | RDIGIT[subperiod]

    # Change 1 into 0
    if action == "select":
        pref_period = pref_period & DIGIT[subperiod]

    # Update or insert    
    savePrefPeriod(meeting_id, pref_period)




"""
getUserCA()

Get UserCA instance if it exists, else, return None
"""

def getUserCA(user_id):
    user_ca = UserCA.objects.filter(user_id=user_id)
    if len(user_ca) > 0:
        return UserCA.objects.get(user_id=user_id)
    else:
        return None


"""
getActiveUserInvitee()
Get list of invitees (whose CAs are active in dms.user_ca) of a user
"""
def getActiveUserInvitee(user_id):
    
    user_ca = UserCA.objects.filter(active="True").values('user_id').query
    active_user_invitee = UserInvitee.objects.filter(invitee_id__in=user_ca)
    return active_user_invitee
      


"""
addUIM()

Add invitees whose CAs are active to dms.user_invitee_meeting upon the submission of meeting config (start)

"""


def addUIM(host_id, meeting_id, invitee_id):
    
    # First check whether the record exists
    check = UserInviteeMeeting.objects.filter(host_id=host_id,meeting_id=meeting_id,invitee_id=invitee_id)
    # If exists, do nothing
    if len(check) > 0:
        pass
    
    # Else, insert it
    else:
        
        # Get the foreign key instances
        host_user = User.objects.get(id=host_id)
        host_user_spade = UserSPADE.objects.get(user_id=host_user)
        
        invitee_user = User.objects.get(id=invitee_id)
        invitee_user_spade = UserSPADE.objects.get(user_id=invitee_user)
        
        meeting_id = Meeting.objects.get(meeting_id=meeting_id)
        
        user_ca = UserCA.objects.get(user_id=invitee_id)
        accept = user_ca.accept
        
        uim = UserInviteeMeeting(host_id=host_user_spade, meeting_id=meeting_id, invitee_id=invitee_user_spade,accept=accept)
        
        uim.save()
    

"""

addAllUIM()

Add all active invitees of a user (host) to UIM
"""

def addAllUIM(user_id, meeting_id):
    user_invitee = getActiveUserInvitee(user_id)
    
    # Convert user_invitee instance into a list of id
    id_list = user_invitee.values_list('invitee_id',flat=True)
    
    # Add every id in the list to UIM
    for invitee_id in id_list:
        addUIM(user_id, meeting_id, invitee_id)
        

"""
getUIMInvitee()

Get all the invitees of a specific meeting in the dms.user_invitee_meeting

"""
def getUIMInvitee(meeting_id):
    uim_invitee = UserInviteeMeeting.objects.filter(meeting_id=meeting_id)
    return uim_invitee


"""
getUIMWithStatus()

Get a list of invitees of a meeting with their status and username to the host

[{invitee_id: INVITEE_ID, available: True, accept: True, status: 1, name: NAME} , {},...]
"""

def getUIMWithStatus(meeting_id,user_id):
    import copy
    uim_invitee = getUIMInvitee(meeting_id)
    uim_dict = uim_invitee.values('invitee_id','available','accept')
    uim_with_status = []
    dict = {}
    for uim in uim_dict:
        invitee_id = uim['invitee_id']
        user_invitee = UserInvitee.objects.get(invitee_id =invitee_id)
        dict = uim
        # Save status
        dict['status'] = user_invitee.invitee_status
        # Save username
        dict['name'] = user_invitee.invitee_id.user_name
        uim_with_status.append(dict)
    return uim_with_status



"""
getInvitation()

Get the invitation of meetings for a certain user (invitee)

"""

def getInvitation(user_id):
    # Get meetings whose column 'invite' is True
    meeting_invite = Meeting.objects.filter(invite='True').values('meeting_id').query
    
    uim = UserInviteeMeeting.objects.filter(invitee_id=user_id,meeting_id__in=meeting_invite)
    
    return uim


"""
getInvitationMeeting()

"""
def getInvitationMeeting(user_id,meeting_id):
    uim = getInvitation(user_id)
    uim = uim.filter(meeting_id=meeting_id)
    return uim


"""
updateUIM()

Update dms.user_invitee_meeting.accept 
Invitee's action
"""

def updateUIM(invitee_id,meeting_id,accept):
    if accept == 'true':
        accept = 'True'
    if accept == 'false':
        accept = 'False'
    uim = UserInviteeMeeting.objects.get(invitee_id=invitee_id,meeting_id=meeting_id)
    uim.accept = accept
    uim.save()


"""
isVIPDecline()

Determine whether a VIP declined the invitation (dms.user_invitee_meeting.accept=False)

"""
def isVIPDecline(meeting_id, user_id):
    user_invitee = getUserInvitee(user_id)
    vip_invitee = user_invitee.filter(invitee_status=1)
    vip_id_list = vip_invitee.values_list('invitee_id',flat=True)
    uim_invitee = getUIMInvitee(meeting_id)
    result = False
    for invitee in uim_invitee:
        if invitee.invitee_id.user_id.id in vip_id_list:
            if invitee.accept == "False":
                result = True
                break
            
    return result

"""
getStage()

Get the scheduling stage of a current meeting being scheduled

Code mapping:
 0 => conf_period: NULL :: Calculating and generating period
 1 => conf_period: True :: Waiting for host to confirm period using choose_period
 2 => conf_period: False :: Scheduling failed (** waiting for user to cancel or reschedule)
 3 => conf_period: PERIOD :: Period confirmed
 3 => stat_id: ID :: Statistics acquired
 0,1,2 => stat_id: NULL :: (field not available)
 0,1,2 => invite: NULL :: (field not available)
 3 => invite: NULL :: Waiting for host to send invitation, ** reschedule or cancel
 4 => invite: True :: Invitation sent
 5 => invite: False :: Invitation not sent and meeting canceled
 4 => cancel: NULL :: No declination feedback from VIP (** waiting for host to reschedule or cancel)
 6 => cancel: NULL :: ; Declination received but host hasn't yet give response (** waiting for host to reschedule or cancel)
 7 (4) => cancel: True :: One or more VIP declined the invitation, and meeting canceled by host
 8 (4) => cancel: False :: One or more VIP declined the invitation, but meeting continued by host
 9 => reschedule : True :: The meeting will be rescheduled soon. Please wait until ALCC refreshes the meeting configuration.
 
"""
def getStage(meeting_id, user_id):
    meeting = Meeting.objects.get(meeting_id=meeting_id)
    
    if meeting.conf_period == "" :
        return 0
        
    elif meeting.conf_period == "True" :
        return 1
    
    elif meeting.reschedule == "True":
        return 9
    
    elif meeting.conf_period == "False":        
        return 2
    
    elif meeting.conf_period.isdigit() and meeting.invite == "" :
        return 3
    
    elif meeting.conf_period.isdigit() and meeting.invite == "True" and meeting.cancel == "":
        # VIP declination received
        if isVIPDecline(meeting_id, user_id):
            return 6
        
        # No VIP declination received
        else:
            return 4
    
    elif meeting.conf_period.isdigit() and meeting.invite == "False" :
        return 5
    
    elif meeting.conf_period.isdigit() and meeting.invite == "True" and meeting.cancel == "True":
        return 7
    
    elif meeting.conf_period.isdigit() and meeting.invite == "True" and meeting.cancel == "False":
        return 8
    

"""
getMeetingState()

Get the meeting state of any given meeting_id
Return values

# -1: Default
# 0 : Unfinished config :: 
# 1 : Current meeting (neither success nor canceled)       :: This meeting is being scheduled  (operative)
# 2:  Successful meeting before due day                    :: This meeting is successful  (operative)
# 3:  Successful meeting that are due (expired meetings)   :: This meeting is due
# 4   Canceled meeting                                     :: This meeting has been canceled
"""
def getMeetingState(meeting_id, user_id):
    meeting_state = -1
    
    if getUnfinishedConfig(user_id):
        unfinished = getUnfinishedConfig(user_id)
        if meeting_id == unfinished.meeting_id:
            meeting_state = 0

    if meeting_id in getCurrentMeeting(user_id).values_list('meeting_id',flat=True):
        meeting_state = 1
    
    if meeting_id in getMeetingSuccessList().values_list('meeting_id',flat=True):
        meeting_state = 2
      
    if meeting_id in getDueMeetingSuccessList().values_list('meeting_id',flat=True):
        meeting_state = 3 
               
    if meeting_id in getMeetingCanceledList().values_list('meeting_id',flat=True):
        meeting_state = 4     

    return meeting_state

"""
getChoosePeriod()

Interact helper function
Stage code: 1
Waiting for host to choose confirmed period from choose period
Return choose_tuple_list [( time_format1, period1 ), (time_format2, period2) , ...]

"""
 
def getChoosePeriod(meeting_id):
    meeting = Meeting.objects.get(meeting_id=meeting_id)
    choose_period = meeting.choose_period
    choose_list = choose_period.split(";")
    choose_tuple_list = []
    
    for period_str in choose_list:
        period = int(period_str)
        time = period2Time(period)
        
        # Append the tuple (time, period) into choose_tuple_list
        choose_tuple_list.append((time, period))
        
    return choose_tuple_list


"""
updateConfPeriod()

Update dms.meeting.conf_period with the period that is chosen by the host
"""

def updateConfPeriod(meeting_id,choose_period):
    meeting = Meeting.objects.get(meeting_id=meeting_id)
    meeting.conf_period = choose_period
    meeting.save()


"""
updateInvite()

Update dms.meeting.invite with the value from GET

"""

def updateInvite(meeting_id, invite):
    
    invite = invite.strip()
    if invite == "true" or invite == "false":
        if invite == "true":
            invite = "True"
        if invite == "false":
            invite = "False"
            
        meeting = Meeting.objects.get(meeting_id=meeting_id)
        meeting.invite = invite
        meeting.save()


"""
updateCancel()

Update dms.meeting.cancel with the value from GET
if cancel is "force", then direcly add the meeting to dms.meeting_canceled and add host_id to MSA so that ALCC will shut it down

"""

def updateCancel(meeting_id, user_id, cancel):
    cancel = cancel.strip()
    
    if cancel == "true" or cancel == "false":
        
        if cancel == "true":
            cancel = "True"
            
        if cancel == "false":
            cancel = "False"
            
        meeting = Meeting.objects.get(meeting_id=meeting_id)
        meeting.cancel = cancel
        meeting.save()
    
    ### Force cancel ####
    # Directly add the meeting to dms.meeting_canceled
    elif cancel == "force":
        
        addToMeetingCanceled(meeting_id, user_id)
        addToMSA(user_id, meeting_id, 'False')

"""
addToMeetingCanceled()

Force cancel
Add the meeting to dms.meeting_canceled
"""

def addToMeetingCanceled(meeting_id, host_id):
    
    # If meeting does not exist in dms.meeting_canceled
    if not isMeetingCanceled(meeting_id):
        meeting = Meeting.objects.get(meeting_id=meeting_id)
        user_spade = UserSPADE.objects.get(user_id=host_id)
        meeting_canceled = MeetingCanceled(meeting_id=meeting, host_id=user_spade, stage="FC", date="2000-01-01")
        meeting_canceled.save()


"""
isMeetingCanceled()
Determine whether a meeting exists in dms.meeting_canceled

"""
def isMeetingCanceled(meeting_id):
    
    meeting_canceled = MeetingCanceled.objects.filter(meeting_id=meeting_id)
    
    if len(meeting_canceled) > 0:
        return True
    else:
        return False

"""

updateReschedule()

Update dms.meeting.reschedule to True
"""
def updateReschedule(meeting_id):
    meeting = Meeting.objects.get(meeting_id=meeting_id)
    meeting.reschedule = True
    meeting.save()




"""
addToMSA()

Add the meeting_id and host_id into dms.msa so that ALCC can start the MSA

"""

def addToMSA(host_id, meeting_id, active):
    check = MSA.objects.filter(user_id=host_id)
    if len(check) > 0:
        pass
    else:
        meeting = Meeting.objects.get(meeting_id=meeting_id)
        user = UserSPADE.objects.get(user_id=host_id)
        msa = MSA(user_id=user,meeting_id=meeting,active=active)
        msa.save()
        
        
def addToCA(user_id, active):
    
    check = CA.objects.filter(user_id=user_id)
    
    if len(check) > 0:
        pass
    
    else:
        user = UserSPADE.objects.get(user_id=user_id)
        ca = CA(user_id=user,active=active)
        ca.save()


"""
getMeetingFailed()

Get meetings that failed

"""
   
def getMeetingFailed(user_id):
    
    # Get valid meetings (exclude unfinished or current meeting)
    meeting_valid = Meeting.objects.filter(length__gt=0).values('meeting_id').query
    meeting_success = MeetingSuccess.objects.all().values('meeting_id').query
    meeting_failed = Meeting.objects.filter(meeting_id__in=meeting_valid).exclude(meeting_id__in=meeting_success)
    
    return meeting_failed


def getMeetingSuccess(user_id):
    
    # Get valid meetings (exclude unfinished or current meeting)
    meeting_valid = Meeting.objects.filter(length__gt=0).values('meeting_id').query
    meeting_canceled = MeetingCanceled.objects.all().values('meeting_id').query
    meeting_success = Meeting.objects.filter(meeting_id__in=meeting_valid).exclude(meeting_id__in=meeting_canceled)
    
    return meeting_success
"""
Other methods
############
"""


"""
period2Time()
Convert a interger period (consecutive period) into time format (hh:00 - hh:00)
Only for CONSECUTIVE PERIOD, not COMBINED PERIOD !!!
"""
    
def period2Time(period):
    from agenda.views import dailyPeriod2list
    list = dailyPeriod2list(period)
    start = -1
    end = -1
    counter = 0
    for h in list:
        if start == -1:
            if h == 0:
                start = counter
        else:
            if h == 1:
                end = counter
                break     
        counter += 1
        
    if start == -1:
        start = 0
    if end == -1:
        end = 16
        
    start_time = "%02d:00"%(start+6)
    end_time = "%02d:00"%(end+6)
    time = "%s - %s"%(start_time, end_time)
    return time
    
    
    
"""
combinedPeriod2Time()
Modified from period2Time
Convert Combined Period to time format in list

"""
def combinedPeriod2Time(period):
    times = []
    from agenda.views import dailyPeriod2list
    list = dailyPeriod2list(period)
    onelist = [1 for i in range(0,16)]
    while True:
        if list == onelist:
            break
        start = -1
        end = -1
        counter = 0
        for h in list:
            
            if start == -1:
                if h == 0:
                    # Record the first appearing 0
                    start = counter
                    # Change this first 0 to 1 on this bit
                    list[counter] = 1
            else:
                if h == 1:
                    end = counter
                    break
                else:
                    # Change following 0 to 1 on this bit
                    list[counter] = 1
                    
            counter += 1
            
        if start == -1:
            start = 0
        if end == -1:
            end = 16
            
        start_time = "%02d:00"%(start+6)
        end_time = "%02d:00"%(end+6)
        time = "%s - %s"%(start_time, end_time) 
        times.append(time)
        
    return times


"""
formatDate()
Convert yyyymmmdd to datetime.date() instance
"""

def formatDate(date):
    import datetime
    date = str(date)
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])
    
    format_date = datetime.date(year,month,day)
    return format_date


"""
formatDateList()
Convert list of yyyymmmdd to datetime.date() instance list
"""    
def formatDateList(date_list):
    if len(date_list)>0:
        format_date_list = []
        for date in date_list:
            format_date = formatDate(date)
            format_date_list.append(format_date)
        return format_date_list
    else:
        return date_list
    
    
    
    