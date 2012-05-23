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
    conf_period = models.IntegerField(null=True) # True | False | NULL | Period
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
    period = models.IntegerField()
    stage = models.CharField(max_length=24) # GEN | INVT | FB
    reason = models.CharField(max_length=765)
    class Meta:
        db_table = u'meeting_canceled'

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
"""
def getMeetingSuccessList():
    meeting_canceled = MeetingCanceled.objects.all().values('meeting_id').query
    meeting_list = MeetingSuccess.objects.exclude(meeting_id__in=meeting_canceled)
    return meeting_list


