from django.db import models
from django.contrib.auth.models import User
from user.models import UserSPADE

"""
UserAgenda

# Model of dms.user_agenda
"""

class UserAgenda(models.Model):
    
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(UserSPADE, db_column="user_id")
    date = models.DateField()
    daily_period = models.IntegerField()
    pref_period = models.IntegerField()
    best_period = models.IntegerField()
    event_id = models.ForeignKey('Event', db_column="event_id", null= True)
    
    class Meta:
        db_table = u'user_agenda'
    

"""
Event

# Model of dms.event
"""

class Event(models.Model):
    event_id = models.IntegerField(primary_key=True)
    p1 = models.CharField(max_length=765)
    p2 = models.CharField(max_length=765)
    p3 = models.CharField(max_length=765)
    p4 = models.CharField(max_length=765)
    p5 = models.CharField(max_length=765)
    p6 = models.CharField(max_length=765)
    p7 = models.CharField(max_length=765)
    p8 = models.CharField(max_length=765)
    p9 = models.CharField(max_length=765)
    p10 = models.CharField(max_length=765)
    p11 = models.CharField(max_length=765)
    p12 = models.CharField(max_length=765)
    p13 = models.CharField(max_length=765)
    p14 = models.CharField(max_length=765)
    p15 = models.CharField(max_length=765)
    p16 = models.CharField(max_length=765)
    
    class Meta:
        db_table = u'event'


"""
isDateEmpty()
Determine whether a user's agenda on a certain date is empty by querying dms.user_agenda

"""

def isDateEmpty(user_id,date):
    agenda = UserAgenda.objects.filter(user_id=user_id, date=date)
    if len(agenda) > 0:
        return False
    else:
        return True 