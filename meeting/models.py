from django.db import models
from django.contrib.auth.models import User
from user.models import UserSPADE, UserConfig

from django import forms


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
    LENGTH_CHOICES = (
        (1,'1 hour'),
        (2,'2 hours'),
        (3,'3 hours'),
        (4,'4 hours'), 
        (5,'5 hours'),  
    )
    
    length = models.IntegerField(choices=LENGTH_CHOICES)
    day_range = models.CharField(max_length=1500)
    pref = models.IntegerField()
    topic = models.CharField(max_length=1500)
    location = models.CharField(max_length=1500,blank=True)
    
    SEARCH_BIAS_CHOICES = (
        ('AVERAGE_IDLE','Average idleness'),
        ('DAY_LENGTH','Day length'),
    )    
    search_bias = models.CharField(max_length=60,choices=SEARCH_BIAS_CHOICES,blank=True)
    
    DELIMIT_CHOICES = (
        (1,'1'), (2,'2'), (3,'3'), (4,'4'), (5,'5'), (6,'6'), (7,'7'), (8,'8'),
    )    
    delimit = models.IntegerField(null=True,choices=DELIMIT_CHOICES,blank=True)
    
    CONF_METHOD_CHOICES = (
        ('AUTO','Automatic'),
        ('PROMPT','Ask me'),
    )        
    conf_method = models.CharField(max_length=60,choices=CONF_METHOD_CHOICES,blank=True)
    
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
    dlist = day_range.split(';')
    # Remove empty element
    
    return dlist

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
    start_time = "%02d:00"%(start+6)
    end_time = "%02d:00"%(end+6)
    time = "%s - %s"%(start_time, end_time)
    return time
    
