import json
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, Http404, HttpResponseRedirect as redirect_to
from .models import Notification
# Create your views here.
@login_required
def all(request):
	head_title = "Notifications"
	notifications = Notification.objects.all_for_user(request.user)
	# notifications = Notification.objects.filter(recipient=request.user)
	context = {
		"notifications":notifications,
		"head_title":head_title
	}
	template = "notifications/all.html"
	return render(request, template, context)

@login_required
def read(request,id):
	try:
		next_url = request.GET.get('next', None)
		notification = Notification.objects.get(id=id)
		if notification.recipient == request.user:
			notification.read=True
			notification.save()
			if next_url is not None:
				return redirect_to(next_url)
			else:
				return redirect_to(reverse("notifications_all"))
		else:
			raise Http404
	except:
		return redirect_to(reverse("notifications_all"))

@login_required
def read_all(request):
	try:
		notifications = Notification.objects.all_unread(request.user)
		for notification in notifications:
			if notification.recipient == request.user:
				notification.read=True
				notification.save()
			else:
				raise Http404
		return redirect_to(reverse("notifications_all"))
	except:
		return redirect_to(reverse("notifications_all"))

@login_required
def get_notification_ajax(request):
	if request.is_ajax() and request.method == "POST":
		notifications = Notification.objects.all_unread(request.user)
		count = notifications.count()
		notes = []
		for note in notifications:
			notes.append(str(note.get_link()))
		data = {
			"notifications": notes,
			"count":count,
		}
		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type='application/json')	
	else:
		raise Http404

@login_required
def get_notification_count_ajax(request):
	if request.is_ajax() and request.method == "POST":
		notifications = Notification.objects.all_unread(request.user)
		count = notifications.count()
		data = {
			"count":count,
		}
		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type='application/json')	
	else:
		raise Http404