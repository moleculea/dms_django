from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Model of dms.user_spade, user table for spade
# User profile of django.contrib.auth.models.User

class UserSPADE(models.Model):
    
    user_id = models.OneToOneField(User,primary_key=True,db_column="user_id")
    user_name = models.CharField(max_length=384)

    class Meta:
        db_table = u'user_spade'   


# Signal function
# Create a record of the same user_id and user_name to auth_user.id and auth_user.username upon post_save (user registration)
def create_user_spade(sender, instance, created, **kwargs):
    if created:
        user_spade = UserSPADE.objects.create(user_id=instance.id,user_name=instance.username)
        user_spade.save()

post_save.connect(create_user_spade, sender=User)
    
