from django.db import models
from django.contrib.auth.models import User
from user.models import UserSPADE
from django import forms

import sys
sys.path.append('/home/anshichao/dms/spade/Algorithms')
from DIGIT import *

"""
UserAgenda

# Model of dms.user_agenda
"""

class UserAgenda(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(UserSPADE, db_column="user_id")
    date = models.DateField()
    daily_period = models.IntegerField()
    pref_period = models.IntegerField()
    best_period = models.IntegerField()
    event_id = models.ForeignKey('Event', db_column="event_id", null=True)
    
    class Meta:
        db_table = u'user_agenda'
    

"""
Event

# Model of dms.event
"""

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
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
EventForm

Used to submit event for a SINGLE one-hour sub-period
"""
class EventForm(forms.Form):
    
    event = forms.CharField(required=False, max_length=765, widget=forms.TextInput(attrs={'size':'40','maxlength':'765'} ))
    
    

"""
isDateEmpty()
Determine whether a user's agenda on a certain date is empty by querying dms.user_agenda
date can be either a "yyyy-mm-dd" string or a datetime.date instance
"""

def isDateEmpty(user_id,date):
    agenda = UserAgenda.objects.filter(user_id=user_id, date=date)
    if len(agenda) > 0:
        return False
    else:
        return True


"""
isEventEmpty()


"""
def isEventEmpty(user_id,date):
    agenda = UserAgenda.objects.filter(user_id=user_id, date=date)
    if len(agenda) > 0:
        agenda = UserAgenda.objects.get(user_id=user_id, date=date)
        if agenda.event_id:
            return False
        else:
            return True
    else:
        return True


"""
getPeriod()
Get the period of a certain date for a user
Before calling this function must use isDateEmpty to validate that the date exists for the user

    return value: agenda
        # daily_period: agenda.daily_period
        # pref_period: agenda.pref_period
        # best_period: agenda.best_period
"""

def getPeriod(user_id,date):
    agenda = UserAgenda.objects.get(user_id=user_id, date=date)
    return agenda


"""
getEvent()
Before calling this function must use isEventEmpty to validate that the date exists for the user

"""
def getEvent(user_id,date):
    agenda = UserAgenda.objects.get(user_id=user_id, date=date)
    event = agenda.event_id
    return event

"""
saveDailyPeriod()
Save a daily period to a specific date of a user
"""

def saveDailyPeriod(id, user_id, date, daily_period):
    
    # Update
    if id:
        agenda = UserAgenda.objects.get(pk=id)
        agenda.daily_period = daily_period
        agenda.save()
        
    # Insert
    else:
        user = User(id=user_id)
        user_spade = UserSPADE(user_id=user)
        agenda = UserAgenda(user_id=user_spade, date=date, daily_period=daily_period)
        agenda.save()


"""
saveTypePeriod()
Save a pref_period/best_period to a specific date of a user
"""

def saveTypePeriod(id, user_id, date, pref_period, best_period):
    
    # Update
    if id:
        agenda = UserAgenda.objects.get(pk=id)
        agenda.pref_period = pref_period
        agenda.best_period = best_period
        agenda.save()

    # Insert
    else:
        user = User(id=user_id)
        user_spade = UserSPADE(user_id=user)
        agenda = UserAgenda(pk=id, user_id=user_spade, date=date, pref_period = pref_period, best_period = best_period)
        agenda.save()


"""
saveEvent()
Save event
"""

def saveEvent(user_id, date, event, subperiod):
    
    # Insert new event
    if isEventEmpty(user_id, date):
        
        # Insert date and event
        if isDateEmpty(user_id,date):
            # Insert event to dms.event
            event = instantiateEvent(subperiod,event)
            event.save()
            
            # Insert date to dms.user_agenda, with foreign key to event
            user = User(id=user_id)
            user_spade = UserSPADE(user_id=user)
            agenda = UserAgenda(user_id=user_spade,date=date,event_id=event)
            agenda.save()
            
        # Update date and insert event
        else:
            # Insert event to dms.event
            event = instantiateEvent(subperiod,event)
            event.save()
            
            # Get primary key for agenda instance
            agenda = getPeriod(user_id, date)
            id = agenda.id
            
            # Update date to dms.user_agenda, with foreign key to event
            user = User(id=user_id)
            user_spade = UserSPADE(user_id=user)
            agenda = UserAgenda(pk=id,user_id=user_spade,date=date,event_id=event)
            agenda.save()

    # Update event
    else:
        agenda = getPeriod(user_id, date)
        # Get the event instance
        e = agenda.event_id
        e = instantiateEvent(subperiod,event,e)
        e.save()
        
    
"""
instantiateEvent()
Instantiate Event class with subperiod and event
"""
def instantiateEvent(subperiod,event,inst=None):

    if inst:
        cmd = "inst.p%s = event"%(subperiod+1)
        exec(cmd)
        return inst
        
    else:
        sublist = [u'' for i in range(0,16)]
        sublist[subperiod] = event
        instance = Event(p1=sublist[0],p2=sublist[1],p3=sublist[2],p4=sublist[3],p5=sublist[4],p6=sublist[5],p7=sublist[6],p8=sublist[7],p9=sublist[8],p10=sublist[9],p11=sublist[10],p12=sublist[11],p13=sublist[12],p14=sublist[13],p15=sublist[14],p16=sublist[15])
        return instance
    


"""
changeDailyPeriod()
Change an one-hour sub-period of a date into "idle" or "occupied"

subperiod is an index from 0 to 15 indicating 16 different hourly sub-periods

"""

def changeDailyPeriod(user_id, date, action, subperiod):
    daily_period = 0
    id = None;
    if action == "occupy":
        if isDateEmpty(user_id, date):
            daily_period = daily_period | RDIGIT[subperiod]
            
        else:
            agenda = getPeriod(user_id, date)
            id = agenda.id
            daily_period = agenda.daily_period
            daily_period = none2Zero(daily_period)
            daily_period = daily_period | RDIGIT[subperiod]

    
    if action == "idle":
        agenda = getPeriod(user_id, date)
        id = agenda.id
        daily_period = agenda.daily_period
        daily_period = none2Zero(daily_period)
        daily_period = daily_period & DIGIT[subperiod]

    # Update or insert    
    saveDailyPeriod(id, user_id, date, daily_period)

"""

changeTypePeriod()

Change pref_period or best_period according to type given as an argument
Make sure pref_period and best_period don't conflict with each other

Totally DIFFERENT from changeDailyPeriod : digit expressions of daily_period and pref_period/best_period are opposite
"""

def changeTypePeriod(user_id, date, action, subperiod, type):
    
    pref_period = REVERSE
    best_period = REVERSE
    id = None
    
    # To change 1 into 0 (expand period)
    if action == "occupy":
        if isDateEmpty(user_id, date):
            if type == "pref":
                pref_period = pref_period & DIGIT[subperiod]
                
            if type == "best":
                best_period = best_period & DIGIT[subperiod]
                
        else:
            agenda = getPeriod(user_id, date)
            id = agenda.id
            
            pref_period = agenda.pref_period
            best_period = agenda.best_period

            pref_period = none2Reverse(pref_period)
            best_period = none2Reverse(best_period)
            
            if type == "pref":
                # Change 1 into 0
                pref_period = pref_period & DIGIT[subperiod]
                
                # Meantime, revert the sub-period on best_period to avoid conflict
                # Change 0 into 1

                best_period = best_period | RDIGIT[subperiod]    
                
            if type == "best":
                # Change 1 into 0
                best_period = best_period & DIGIT[subperiod]
                
                # Meantime, revert the sub-period on pref_period to avoid conflict
                # Change 0 into 1

                pref_period = pref_period | RDIGIT[subperiod]

    # To change 0 into 1 (cut period)
    if action == "idle":
        if isDateEmpty(user_id, date):
            if type == "pref":
                pref_period = pref_period | RDIGIT[subperiod]
                
            if type == "best":
                best_period = best_period | RDIGIT[subperiod]
                
        else:
            agenda = getPeriod(user_id, date)
            id = agenda.id
            
            pref_period = agenda.pref_period
            best_period = agenda.best_period

            pref_period = none2Reverse(pref_period)
            best_period = none2Reverse(best_period)
            
            if type == "pref":
                # Change 0 into 1
                pref_period = pref_period | RDIGIT[subperiod]
                
                # Meantime, revert the sub-period on best_period to avoid conflict
                # Change 1 into 0
                #best_period = best_period & DIGIT[subperiod]    
                
            if type == "best":
                # Change 0 into 1
                best_period = best_period | RDIGIT[subperiod]
                
                # Meantime, revert the sub-period on pref_period to avoid conflict
                # Change 1 into 0
                #pref_period = pref_period & DIGIT[subperiod]         
     
    # Update or insert pref_period/best_period           
    saveTypePeriod(id, user_id, date, pref_period, best_period)                
 
"""
none2Zero()
If the period is None, convert it into 0
"""
def none2Zero(period):
    if period == None:
        period = 0
    return period
 
                   
"""
none2Reverse()
If the period is None, convert it into REVERSE and return it
Else, return the period unchanged
"""
def none2Reverse(period):
    if period == None:
        period = REVERSE
    return period

"""
isZero()
Determine whether an one-hour sub-period of the given period is zero
"""
def isZero(period,subperiod):
    if period | DIGIT[subperiod] == DIGIT[subperiod]:
        return True
    else:
        return False
    
    