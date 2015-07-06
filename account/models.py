from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from tasks.models import TodoList

# Create your models here.
class UserProfile(models.Model):
    user      = models.OneToOneField(User)
    bio       = models.TextField(null=True, blank=True)
    timezone = models.CharField(max_length=120,default = 'UTC')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated   = models.DateTimeField(auto_now=True, auto_now_add=False)

    facebook =models.CharField(
        max_length=320, 
        null=True, 
        blank=True, 
        verbose_name='Facebook profile URL'
        )
    twitter =models.CharField(
        max_length=320, 
        null=True, 
        blank=True, 
        verbose_name='Twitter handle'
        )

    def __unicode__(self):
        return self.user.username

    def full_name(self):
    	return "%s, %s" %(self.user.last_name, self.user.first_name)



def new_user_receiver(sender, instance, created, *args, **kwargs):
	if created:
        # create user profile
		new_profile, is_created = UserProfile.objects.get_or_create(user=instance)

        # notify.send(
        #     instance,
        #     verb='New User created.',
        #     recipient=MyUser.objects.get(username="admin"))
    
post_save.connect(new_user_receiver, sender=User)