from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import mark_safe, truncatechars

from .signals import notify
# Create your models here.

class NotificationQuerySet(models.query.QuerySet):
	def get_user(self, user):
		return self.filter(recipient=user)

	def mark_targetless_as_read(self,user):
		qs = self.get_user(user).unread()
		qs_targetless = qs.filter(target_object_id=None)
		if qs_targetless:
			qs_targetless.update(read=True)

	def mark_all_as_read(self,user):
		qs = self.get_user(user).unread()
		qs.update(read=True)

	def mark_all_as_unread(self,user):
		qs = self.get_user(user).read()
		qs.update(read=False)

	def unread(self):
		return self.filter(read=False)

	def read(self):
		return self.filter(read=True)

	def recent(self):
		return self.unread()[:5]

class NotificationManager(models.Manager):
	def get_queryset(self):
		return NotificationQuerySet(self.model, using=self._db)

	def all_unread(self,user):
		return self.get_queryset().get_user(user).unread()

	def all_read(self,user):
		return self.get_queryset().get_user(user).read()

	def all_for_user(self,user):
		self.get_queryset().mark_targetless_as_read(user)
		return self.get_queryset().get_user(user)

class Notification(models.Model):
	sender_content_type = models.ForeignKey(ContentType, related_name='notify_sender')
	sender_object_id    = models.PositiveIntegerField()
	sender_object       = GenericForeignKey("sender_content_type", "sender_object_id")
	
	action_content_type = models.ForeignKey(ContentType, related_name='notify_action',null=True, blank=True)
	action_object_id    = models.PositiveIntegerField(null=True, blank=True)
	action_object       = GenericForeignKey("action_content_type", "action_object_id")
	
	target_content_type = models.ForeignKey(ContentType, related_name='notify_target',null=True, blank=True)
	target_object_id    = models.PositiveIntegerField(null=True, blank=True)
	target_object       = GenericForeignKey("target_content_type", "target_object_id")
	
	verb                = models.CharField(max_length=255)
	recipient           = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications')
	timestamp           = models.DateTimeField(auto_now=False, auto_now_add=True)
	read                = models.BooleanField(default=False)

	objects = NotificationManager()

	class Meta:
		ordering = ['-timestamp']

	def __unicode__(self):
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = None

		context = {
			"sender": self.sender_object,
			"action": truncatechars(self.action_object,30),
			"target": self.target_object,
			"target_url":target_url,
			"verb": self.verb,
			"recipient": self.recipient,
			"verify_read": reverse('notifications_read', kwargs={"id":self.id,})
		}
		if self.target_object:
			if self.action_object:
				if target_url:
					return mark_safe('<a href="%(verify_read)s?next=%(target_url)s">%(sender)s %(verb)s %(target)s</a>' %context)
				return '%(sender)s %(verb)s %(target)s' %context
			return '%(sender)s %(verb)s %(target)s' %context
		return '%(sender)s %(verb)s' %context


	def get_link(self):
		try:
			target_url = self.target_object.get_absolute_url()
		except:
			target_url = reverse('notifications_all')

		context = {
			"sender": self.sender_object,
			"action": truncatechars(self.action_object,30),
			"target": self.target_object,
			"target_url":target_url,
			"verb": self.verb,
			"recipient": self.recipient,
			"verify_read": reverse('notifications_read', kwargs={"id":self.id,})
		}
		if self.target_object:
			return mark_safe('<a href="%(verify_read)s?next=%(target_url)s">%(sender)s %(verb)s %(target)s</a>' %context)
		return '<a href="%(verify_read)s?next=%(target_url)s">%(sender)s %(verb)s</a>' %context
	

def new_notification(sender, **kwargs):
	kwargs.pop("signal", None)
	recipient      = kwargs.pop("recipient")
	verb           = kwargs.pop("verb")
	affected_users = kwargs.pop("affected_users", None)

	if affected_users is not None:
		for user in affected_users:
			if user == sender:
				pass
			else:
				new_note = Notification(
					verb                = verb, #smart text
					recipient           = user,
					sender_content_type = ContentType.objects.get_for_model(sender),
					sender_object_id    = sender.id,)
				for opt in ("target", "action"):
					try:
						obj = kwargs[opt]
						if obj is not None:
							setattr(new_note, "%s_content_type" %opt, ContentType.objects.get_for_model(obj))
							setattr(new_note, "%s_object_id" %opt, obj.id)
					except:
						pass
				new_note.save()
	else:
		new_note = Notification(
			verb                = verb, #smart text
			recipient           = recipient,
			sender_content_type = ContentType.objects.get_for_model(sender),
			sender_object_id    = sender.id,)
		for opt in ("target", "action"):
			try:
				obj = kwargs[opt]
				if obj is not None:
					setattr(new_note, "%s_content_type" %opt, ContentType.objects.get_for_model(obj))
					setattr(new_note, "%s_object_id" %opt, obj.id)
			except:
				pass
		new_note.save()
notify.connect(new_notification)