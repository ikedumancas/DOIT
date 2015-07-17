from django.contrib import admin

from .models import Notification
# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'recipient', 'timestamp']
	class Meta:
		model = Notification

admin.site.register(Notification, NotificationAdmin)