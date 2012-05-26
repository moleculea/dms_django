from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

"""
UserSPADE

# Model of dms.user_spade, user table for spade
# User profile of django.contrib.auth.models.User

"""

class UserSPADE(models.Model):
    
    user_id = models.OneToOneField(User, primary_key=True, db_column="user_id")
    user_name = models.CharField(max_length=384)

    class Meta:
        db_table = u'user_spade'   

"""
UserConfig

# Model of dms.user_config

"""

class UserConfig(models.Model):
    
    user_id = models.OneToOneField(User, primary_key=True, db_column="user_id")
    msa_id = models.ForeignKey('meeting.UserMSA', db_column="msa_id", null=True, related_name='+')
    ca_id = models.ForeignKey('meeting.UserMSA', db_column="ca_id", null=True, related_name='+')
    pref_period = models.IntegerField(null=True)
    best_period = models.IntegerField(null=True)
    
    class Meta:
        db_table = u'user_config'


"""
UserInvitee

# Model of dms.user_invitee

"""
class UserInvitee(models.Model):
    
    id = models.AutoField(primary_key=True)
    host_id = models.ForeignKey('UserSPADE', db_column="host_id", related_name='+')
    invitee_id = models.ForeignKey('UserSPADE', db_column="invitee_id", related_name='+')
    invitee_status = models.IntegerField(null=True)
    
    class Meta:
        db_table = u'user_invitee'
        

"""
Message

# Model of dms.message

"""
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,db_column="user_id", related_name='+')
    content_id = models.ForeignKey('Content',db_column="content_id", related_name='+')
    uri = models.CharField(max_length=300)
    read = models.CharField(max_length=15)
    class Meta:
        db_table = u'message'

"""
Content

# Model of dms.content

"""
class Content(models.Model):
    content_id = models.IntegerField(primary_key=True,db_column="content_id")
    content = models.CharField(max_length=150, db_column="content")
    class Meta:
        db_table = u'content'


"""
# Model methods

"""

def getUserConfig(user_id):
    config = UserConfig.objects.get(user_id=user_id)
    return config


"""
getUserInvitee()
Retun UserInvitee instance

"""
def getUserInvitee(host_id):
    user_invitee = UserInvitee.objects.filter(host_id=host_id)
    return user_invitee


"""
getUserInviteeIDList()

Return a list of invitee id
"""
def getUserInviteeIDList(host_id):
    user_invitee = UserInvitee.objects.filter(host_id=host_id).values_list('invitee_id',flat=True)
    return user_invitee

"""
saveUserInvitee()
Save (insert) user invitee 
"""
def saveUserInvitee(host_id,invitee_id):
    # If empty, insert
    if isUserInviteeEmpty(host_id,invitee_id):
        host_id = UserSPADE.objects.get(user_id=host_id)
        invitee_id = UserSPADE.objects.get(user_id=invitee_id)
        
        user_invitee = UserInvitee(host_id=host_id,invitee_id=invitee_id,invitee_status=0)
        user_invitee.save()
        
    # If not empty, do nothing  
    else:
        pass

"""
updateInviteeStatus()
Update user_invitee.invitee_status

"""

def updateInviteeStatus(host_id,invitee_id,vip=True):
    user_invitee = UserInvitee.objects.get(host_id=host_id,invitee_id=invitee_id)
    # Make it VIP
    if vip:
        user_invitee.invitee_status = 1
        user_invitee.save()
        
    # Make it Non-VIP
    else:
        user_invitee.invitee_status = 0
        user_invitee.save()

"""

deleteUserInvitee()

Delete a specific invitee from user_invitee

"""

def deleteUserInvitee(host_id,invitee_id):
    user_invitee = UserInvitee.objects.get(host_id=host_id,invitee_id=invitee_id)
    user_invitee.delete()
    
    
def isUserInviteeEmpty(host_id,invitee_id):
    user_invitee = UserInvitee.objects.filter(host_id=host_id,invitee_id=invitee_id)
    if len(user_invitee) > 0:
        return False
    else:
        return True

    
def getUserMessage(user_id):    
    message = Message.objects.filter(user_id=user_id).order_by('-id')
    return message
  
  
  
def readMessage(message_id):
    message = Message.objects.get(id=message_id)
    message.read = "True"
    message.save()
    
"""
# Signal processing #

"""

"""
create_user_spade()

# Signal function for UserSPADE
# Create a record of the same user_id and user_name to auth_user.id and auth_user.username upon post_save (user registration)

# Abstract:
    User ==> UserSPADE
"""

def create_user_spade(sender, instance, created, **kwargs):
    if created:
        user_spade = UserSPADE.objects.create(user_id=instance.id,user_name=instance.username)
        user_spade.save()
        
# Listening to post_save signals
post_save.connect(create_user_spade, sender=User)


"""
create_user_config()

# Signal function for UserConfig
# Create a record of the same user_id to user_spade.id upon post_save (user registration)

# Abstract:
    UserSPADE ==> UserConfig
"""

def create_user_config(sender, instance, created, **kwargs):
    if created:
        user_config = UserConfig.objects.create(user_id=instance.user_id)
        user_config.save()

# Listening to post_save signals
post_save.connect(create_user_config, sender=UserSPADE)
