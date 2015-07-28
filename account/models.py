import datetime
import string
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from tasks.models import Todo, TodoList

# Create your models here.
class UserProfile(models.Model):
    user      = models.OneToOneField(User)
    bio       = models.TextField(null=True, blank=True)
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
    	return string.capwords("%s, %s" %(self.user.last_name, self.user.first_name))



def new_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # create user profile
        new_profile, is_created = UserProfile.objects.get_or_create(user=instance)
        try:
            now = datetime.date.today()
            sample_list = TodoList.objects.create_list(user=instance, title='Welcome! Sample list')
            sample_task = Todo.objects.create_todo(user=instance, title='This is a sample task.', list_slug=sample_list.slug)
            sample_task = Todo.objects.create_todo(user=instance, title='This is a sample task with due date.', list_slug=sample_list.slug)
            sample_task.due_date = now
            sample_task.save()
            sample_task = Todo.objects.create_todo(user=instance, title='This is a sample task with priority "critical". The default priority of a task is "Normal"', list_slug=sample_list.slug)
            sample_task.priority = "critical"
            sample_task.due_date = now
            sample_task.save()
            sample_task = Todo.objects.create_todo(user=instance, title='This is a sample task with priority "minor".', list_slug=sample_list.slug)
            sample_task.priority = "minor"
            sample_task.due_date = now
            sample_task.save()
            sample_task = Todo.objects.create_todo(user=instance, title='This is a sample task with description. Press edit(pencil icon below) to see the description.', list_slug=sample_list.slug)
            sample_task.description = "Orayt! Rock 'n Roll to the world!"
            sample_task.due_date = now
            sample_task.save()
            sample_task = Todo.objects.create_todo(user=instance, title='This is a sample task marked as done. Press the check icon to change status.', list_slug=sample_list.slug)
            sample_task.status = "done"
            sample_task.due_date = now
            sample_task.save()
        except:
            pass
        # notify.send(
        #     instance,
        #     verb='New User created.',
        #     recipient=MyUser.objects.get(username="admin"))
    
post_save.connect(new_user_receiver, sender=User)