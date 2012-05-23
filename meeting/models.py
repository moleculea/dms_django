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
    length = models.IntegerField()
    day_range = models.CharField(max_length=1500)
    pref = models.IntegerField()
    topic = models.CharField(max_length=1500)
    location = models.CharField(max_length=1500)
    search_bias = models.CharField(max_length=60)
    delimit = models.IntegerField(null=True)
    conf_method = models.CharField(max_length=60)
    
    # Functional columns
    conf_period = models.CharField(max_length=60) # True | False | NULL | Period
    choose_period = models.CharField(max_length=1500)
    invite = models.CharField(max_length=60) # True | False | NULL
    cancel = models.CharField(max_length=15) # True | False | NULL
    reschedule = models.CharField(max_length=15) # True | NULL
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
    
