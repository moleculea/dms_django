from django.db import models
from django.contrib.auth.models import User
from user.models import UserSPADE

class UserAgenda(models.Model):
    
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(UserSPADE,db_column="user_id")
    date = models.DateField()
    daily_period = models.IntegerField()
    pref_period = models.IntegerField()
    best_period = models.IntegerField()
    
    class Meta:
        db_table = u'user_agenda'