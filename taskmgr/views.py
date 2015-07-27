from django.core.urlresolvers import reverse
from django.shortcuts import render

from account.forms import LoginForm, RegisterForm

def home(request):
	if request.user.is_authenticated():
		template = "tasks/materialize.html"
		response = render(request, template, {})
		response.set_cookie('load_list_url', reverse('get_list_info'))
		response.set_cookie('get_task_url', reverse('get_list_tasks'))
		response.set_cookie('reorder_url', reverse('todo_ajax_reorder'))
		return response
	else:
		login_form = LoginForm
		register_form = RegisterForm
		context = {
			"login_form": login_form,
			"register_form": register_form,
		}
		template = "home.html"
		return render(request, template, context)