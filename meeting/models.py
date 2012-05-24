from django.db import models
from django.contrib.auth.models import User
from user.models import UserSPADE, UserConfig

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
    accept = models.CharField(max_length=15) # True (ACCEPT) | False (DECLINE) | NULL (SILENT)
    
    class Meta:
        db_table = u'user_ca'
  
 
"""
UserInviteeMeeting (UIM)

# Model of dms.user_invitee_meeting

"""   
class UserInviteeMeeting(models.Model):
    
    id = models.AutoField(primary_key=True)
    host_id = models.ForeignKey('user.UserSPADE', db_column="user_id", related_name='+')
    meeting_id = models.ForeignKey('Meeting', db_column="user_id", related_name='+')
    invitee_id = models.ForeignKey('user.UserSPADE', db_column="user_id", related_name='+')
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
    meeting = models.ForeignKey('Meeting', unique=True, db_column='meeting_id',related_name='+')
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
    accept = forms.ChoiceField(widget=forms.RadioSelect,choices=ACCEPT_CHOICES)

"""
Model functions

"""

"""
getMeetingSuccessList()
Get list of successful meetings that are not canceled (truly and temporarily successful)
i.e. meetings in dms.meeting_success and not in dms.meeting_canceled

Meeting dates after TODAY will be excluded from the results
"""
def getMeetingSuccessList():
    import datetime
    today = datetime.date.today()
    meeting_canceled = MeetingCanceled.objects.all().values('meeting_id').query
    meeting_list = MeetingSuccess.objects.exclude(meeting_id__in=meeting_canceled).filter(date__gt=today).order_by('date','id')
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

Only ONE unfinished config is allowed to exist in dms.meeting

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
    
    
    
    