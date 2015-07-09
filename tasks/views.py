import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, Http404, HttpResponseRedirect, redirect, render

from .models import TodoList, Todo
from .forms import AddUserToListForm,FullTodoForm, ListForm, ListReorderForm, NoListFullTodoForm, TaskForm, EditListForm
from account.forms import LoginForm, RegisterForm


def home(request):
	if request.user.is_authenticated():
		list_form = ListForm()
		todo_form = TaskForm()
		user = request.user
		user_todo_lists = user.lists.all()

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
				response_data['edit_url'] = reverse('list_edit', kwargs={'list_slug': new_list.slug})
				response_data['archive_url'] = reverse('list_archive', kwargs={'list_slug': new_list.slug})
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
def list_edit(request,list_slug):
	todolist = get_object_or_404(TodoList, slug=list_slug)
	if request.user not in todolist.users.all():
		raise Http404

	users = todolist.users.exclude(id=request.user.id)
	todolistForm = EditListForm(request.POST or None, initial={'title':todolist.title})
	add_user_form = AddUserToListForm(request.POST or None)
	if request.method == 'POST':
		submit = request.POST.get('submit')
		if todolistForm.is_valid() and submit == 'Save Title':
			todolist.title = todolistForm.cleaned_data['title']
			todolist.save()
			return HttpResponseRedirect(request.get_full_path())
		elif add_user_form.is_valid() and submit == 'Add User':
			user = add_user_form.cleaned_data['username']
			todolist.users.add(user)
			return HttpResponseRedirect(request.get_full_path())

	context = {
		'todolistForm':todolistForm,
		'adduserForm':add_user_form,
		'users':users,
		'list':todolist
	}
	template = "tasks/list_edit.html"
	return render(request, template, context)

# @login_required
# def list_add_user(request, list_slug):
# 	context = {
# 		'todolistForm':todolistForm,
# 		'adduserForm':add_user_form,
# 		'users':users,
# 		'list':todolist
# 	}
# 	template = "tasks/list_edit.html"
# 	return render(request, template, context)


@login_required
def list_archive(request, list_slug):
	task_list = get_object_or_404(TodoList, slug=list_slug)
	if task_list.is_created_by(request.user):
		task_list.mark_as_archived()
		if request.is_ajax():
			response_data = {}
			response_data['result'] = 'archived'
			return HttpResponse(
					json.dumps(response_data),
					content_type="application/json"
				)
	else:
		raise Http404
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
	if request.user not in list_users:
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
		user_todo_lists = request.user.lists.all()
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
			
			old_order = old_task.order
			new_order = form.cleaned_data['order']

			if old_order != new_order:
				old_task.change_order_to(new_order)

			task.title = form.cleaned_data['title']
			task.description = form.cleaned_data['description']
			task.status = form.cleaned_data['status']
			task.due_date = form.cleaned_data['due_date']
			task.save()
			
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
	if request.user not in list_users:
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
	if request.user not in list_users:
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
def todo_ajax_reorder(request):
	form = ListReorderForm(request.POST)
	if form.is_valid():
		task_slug = form.cleaned_data['task_slug']
		task = get_object_or_404(Todo, slug=task_slug)

		list_users = task.todolist.users.all()
		if request.user not in list_users:
			raise Http404

		old_order = task.order
		new_order = form.cleaned_data['order']

		if old_order != new_order:
			task.change_order_to(new_order)
		else:
			response_data = {}
			response_data['result'] = 'List is on the same order. Nothing changed.'
			return HttpResponse(
				json.dumps(response_data),
				content_type="application/json"
				)

		response_data = {}
		response_data['result'] = 'reordered'
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
			)

