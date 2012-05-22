from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from meeting.models import UserMSA, UserCA

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
# Model methods

"""

def getUserConfig(user_id):
    config = UserConfig.objects.get(user_id=user_id)
    return config


def displayUserConfig(user_id):
    pass

def updateUserConfig():
    pass

def doUserInvitee():
    pass



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
