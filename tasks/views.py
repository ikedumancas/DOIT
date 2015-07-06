import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, Http404, HttpResponseRedirect, redirect, render

from .models import TodoList, Todo
from .forms import FullTodoForm, ListForm, NoListFullTodoForm, TaskForm
from account.forms import LoginForm, RegisterForm

# Create your views here.
def home(request):
	if request.user.is_authenticated():
		list_form = ListForm()
		todo_form = TaskForm()
		user = request.user
		user_todo_lists = user.todolist_set.all()
		
		context = {
			"todolists":user_todo_lists,
			"list_form":list_form,
			"todo_form":todo_form
		}
		template = "tasks/todo_lists.html"
	else:
		login_form = LoginForm
		register_form = RegisterForm
		context = {
			"login_form": login_form,
			"register_form": register_form,
		}
		template = "home.html"

	return render(request, template, context)


@login_required
def list_create(request):
	if request.method == "POST":
		form = ListForm(request.POST)
		if form.is_valid():
			if request.is_ajax():
				list_title = form.cleaned_data['title']
				new_list = TodoList.objects.create_list(user=request.user, title=list_title)
				response_data = {}
				response_data['title'] = new_list.title
				response_data['slug'] = new_list.slug
				response_data['result'] = 'New list created!'
				return HttpResponse(
					json.dumps(response_data),
					content_type="application/json"
				)
			else:
				list_title = form.cleaned_data['title']
				new_list = TodoList.objects.create_list(user=request.user, title=list_title)
				return redirect('home')

@login_required
def task_create(request):
	if request.method == "POST":
		form = TaskForm(request.POST)
		if form.is_valid():
			if request.is_ajax():
				task_title = form.cleaned_data['title']
				list_slug = form.cleaned_data['todolist']
				new_list = Todo.objects.create_todo(user=request.user, title=task_title, list_slug=list_slug)
				response_data = {}
				response_data['title'] = new_list.title
				response_data['slug'] = new_list.slug
				response_data['edit_url'] = reverse('task_edit', kwargs={'task_slug': new_list.slug})
				response_data['done_url'] = reverse('task_done', kwargs={'task_slug': new_list.slug})
				response_data['archive_url'] = reverse('task_archive', kwargs={'task_slug': new_list.slug})
				response_data['result'] = 'New task created!'
				return HttpResponse(
					json.dumps(response_data),
					content_type="application/json"
				)
			else:
				form = TaskForm(request.POST or None)
				if form.is_valid():
					print form.cleaned_data
					task_title = form.cleaned_data['title']
					list_slug = form.cleaned_data['todolist']
					new_list = Todo.objects.create_todo(user=request.user, title=task_title, list_slug=list_slug)
				return redirect('home')

@login_required
def task_edit(request, task_slug):
	task = get_object_or_404(Todo, slug=task_slug)

	list_users = task.todolist.users.all()
	if not request.user in list_users:
		raise Http404

	old_task = get_object_or_404(Todo, slug=task_slug)
	list_task_count = task.todolist.task_count()
	list_orders = []
	i = 1
	while i <= list_task_count:
		list_orders.append(i)
		i=i+1
	
	if task.todolist.creator == request.user:
		form = FullTodoForm(instance=task)
		user_todo_lists = request.user.todolist_set.all()
		form.fields['todolist'].queryset = user_todo_lists
	else:
		form = NoListFullTodoForm(instance=task)
	if request.method == "POST":
		if task.todolist.creator == request.user:
			form = FullTodoForm(request.POST, instance=task)
		else:
			form = NoListFullTodoForm(request.POST)
		if form.is_valid():
			if task.todolist.creator == request.user:
				task.todolist = form.cleaned_data['todolist']
			
			# Reordering
			reorder = False
			if old_task.order > form.cleaned_data['order']:
				tasks_to_change_order = task.todolist.todo_set.filter(
					order__gte = form.cleaned_data['order'], 
					order__lte = old_task.order
					).exclude(id=task.id)
				old_order_gte_new_order = True
				reorder = True
			elif old_task.order < form.cleaned_data['order']:
				tasks_to_change_order = task.todolist.todo_set.filter(
					order__lte = form.cleaned_data['order'], 
					order__gte = old_task.order
					).exclude(id=task.id)
				old_order_gte_new_order = False
				reorder = True
			else:
				pass
			if reorder:
				for change_order in tasks_to_change_order:
					if old_order_gte_new_order:
						change_order.order = change_order.order + 1
					else:
						change_order.order = change_order.order -1
					change_order.save()

			task.title = form.cleaned_data['title']
			task.description = form.cleaned_data['description']
			task.order = form.cleaned_data['order']
			task.status = form.cleaned_data['status']
			task.due_date = form.cleaned_data['due_date']
			task.save()
			
			subscribe_user = form.cleaned_data['subscribe_user']
			if subscribe_user:
				task.subcribe_user(request.user)
			else:
				task.unsubcribe_user(request.user)
			# full_path = request.get_full_path()
			return redirect('home')

	context = {
		'form':form,
		'list_orders':list_orders
	}
	template = "tasks/task_edit_form.html"
	return render(request, template, context)

@login_required
def task_done(request, task_slug):
	task = get_object_or_404(Todo, slug=task_slug)
	
	list_users = task.todolist.users.all()
	if not request.user in list_users:
		raise Http404

	task.mark_as_done()
	if request.is_ajax():
		response_data = {}
		response_data['link'] = reverse('task_undone', kwargs={'task_slug': task_slug})
		response_data['result'] = 'done'
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)		
	return redirect('home')

@login_required
def task_undone(request, task_slug):
	task = get_object_or_404(Todo, slug=task_slug)

	list_users = task.todolist.users.all()
	if not request.user in list_users:
		raise Http404

	task.mark_as_active()
	if request.is_ajax():
		response_data = {}
		response_data['link'] = reverse('task_done', kwargs={'task_slug': task_slug})
		response_data['result'] = 'undone'
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)
	return redirect('home')

@login_required
def task_archive(request, task_slug):
	task = get_object_or_404(Todo, slug=task_slug)

	list_users = task.todolist.users.all()
	if not request.user in list_users:
		raise Http404

	task.mark_as_archived()
	if request.is_ajax():
		response_data = {}
		response_data['result'] = 'archived'
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)
	return redirect('home')

@login_required
def reorder(request):
	# Reordering
	reorder = False
	if old_task.order > form.cleaned_data['order']:
		tasks_to_change_order = task.todolist.todo_set.filter(
			order__gte = form.cleaned_data['order'], 
			order__lte = old_task.order
			).exclude(id=task.id)
		old_order_gte_new_order = True
		reorder = True
	elif old_task.order < form.cleaned_data['order']:
		tasks_to_change_order = task.todolist.todo_set.filter(
			order__lte = form.cleaned_data['order'], 
			order__gte = old_task.order
			).exclude(id=task.id)
		old_order_gte_new_order = False
		reorder = True
	else:
		pass
	if reorder:
		for change_order in tasks_to_change_order:
			if old_order_gte_new_order:
				change_order.order = change_order.order + 1
			else:
				change_order.order = change_order.order -1
			change_order.save()