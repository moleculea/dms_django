# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models
from django.contrib.auth.models import User


class Ca(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    active = models.CharField(max_length=15)
    class Meta:
        db_table = u'ca'

class Content(models.Model):
    content_id = models.IntegerField(primary_key=True)
    content = models.CharField(max_length=150)
    class Meta:
        db_table = u'content'


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

class Meeting(models.Model):
    meeting_id = models.IntegerField(primary_key=True)
    host = models.ForeignKey(User)
    length = models.IntegerField()
    day_range = models.CharField(max_length=1500)
    pref = models.IntegerField()
    topic = models.CharField(max_length=1500)
    location = models.CharField(max_length=1500)
    search_bias = models.CharField(max_length=60)
    delimit = models.IntegerField()
    conf_method = models.CharField(max_length=60)
    conf_period = models.IntegerField()
    choose_period = models.CharField(max_length=1500)
    invite = models.CharField(max_length=60)
    cancel = models.CharField(max_length=15)
    reschedule = models.CharField(max_length=15)
    stat = models.ForeignKey(MeetingStat)
    class Meta:
        db_table = u'meeting'

class MeetingCanceled(models.Model):
    id = models.IntegerField(primary_key=True)
    meeting = models.ForeignKey(Meeting, unique=True)
    host = models.ForeignKey(User)
    date = models.DateField()
    period = models.IntegerField()
    stage = models.CharField(max_length=24)
    reason = models.CharField(max_length=765)
    class Meta:
        db_table = u'meeting_canceled'

class MeetingStat(models.Model):
    stat_id = models.IntegerField(primary_key=True)
    meeting = models.ForeignKey(Meeting)
    date = models.DateField()
    conf_period = models.IntegerField()
    confirm = models.IntegerField()
    decline = models.IntegerField()
    class Meta:
        db_table = u'meeting_stat'

class MeetingSuccess(models.Model):
    id = models.IntegerField(primary_key=True)
    meeting = models.ForeignKey(Meeting, unique=True)
    host = models.ForeignKey(User)
    date = models.DateField()
    period = models.IntegerField()
    class Meta:
        db_table = u'meeting_success'

class Message(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    content = models.ForeignKey(Content)
    uri = models.CharField(max_length=60)
    read = models.CharField(max_length=15)
    class Meta:
        db_table = u'message'

class Msa(models.Model):
    id = models.IntegerField(primary_key=True)
    meeting = models.ForeignKey(Meeting, unique=True)
    user = models.ForeignKey(User)
    active = models.CharField(max_length=15)
    class Meta:
        db_table = u'msa'

class UserAgenda(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    date = models.DateField()
    daily_period = models.IntegerField()
    pref_period = models.IntegerField()
    best_period = models.IntegerField()
    class Meta:
        db_table = u'user_agenda'

class UserCa(models.Model):
    ca_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    active = models.CharField(max_length=15)
    accept = models.CharField(max_length=15)
    class Meta:
        db_table = u'user_ca'

class UserConfig(models.Model):
    user = models.ForeignKey(User, primary_key=True)
    msa = models.ForeignKey(UserMsa)
    ca = models.ForeignKey(UserCa)
    pref_period = models.IntegerField()
    best_period = models.IntegerField()
    class Meta:
        db_table = u'user_config'


class UserInvitee(models.Model):
    id = models.IntegerField(primary_key=True)
    host = models.ForeignKey(User)
    invitee = models.ForeignKey(User)
    invitee_status = models.IntegerField()
    class Meta:
        db_table = u'user_invitee'

class UserInviteeMeeting(models.Model):
    id = models.IntegerField(primary_key=True)
    host = models.ForeignKey(User)
    meeting = models.ForeignKey(Meeting)
    invitee = models.ForeignKey(User)
    available = models.CharField(max_length=15)
    accept = models.CharField(max_length=15)
    class Meta:
        db_table = u'user_invitee_meeting'

class UserMsa(models.Model):
    msa_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    active = models.CharField(max_length=15)
    class Meta:
        db_table = u'user_msa'

