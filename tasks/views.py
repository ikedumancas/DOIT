import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, Http404, HttpResponseRedirect, redirect, render

from .models import TodoList, Todo
from .forms import AddUserToListForm,FullTodoForm, ListForm, ListReorderForm, ListSlugForm, NoListFullTodoForm, TaskForm, EditListForm
from account.forms import LoginForm, RegisterForm



def get_list_info(request):
	if request.user.is_authenticated():
		user_todo_lists = request.user.lists.all()
		lists = []
		user_lists = []
		today_count = 0
		in_seven_count = 0
		for todolist in reversed(user_todo_lists):
			today_count = today_count + todolist.todo_set.due_today().count()
			in_seven_count = in_seven_count + todolist.todo_set.due_in_seven().count()
			append_this = {
				"title":todolist.title,
				"slug":todolist.slug,
				"count":todolist.active_count()
			}
			user_lists.append(append_this)
		lists.extend(user_lists)
		in_seven_list_info = {
			"title":"Next 7 Days",
			"slug":"in7days",
			"count":in_seven_count
		}
		lists.append(in_seven_list_info)
		today_list_info = {
			"title":"Today",
			"slug":"today",
			"count":today_count
		}
		lists.append(today_list_info)
		json_data = json.dumps(lists)
		return HttpResponse(json_data, content_type='application/json')
	else:
		raise Http404


@login_required
def get_list_tasks(request):
	if request.method == "POST":
		form = ListSlugForm(request.POST)
		if form.is_valid():
			slug = form.cleaned_data['slug']
			if len(slug) < 11:
				todos = []
				if slug == "today":
					taskslist = Todo.objects.due_today().filter(todolist__users=request.user)
					todos.extend(taskslist)
				elif slug == "in7days":
					taskslist = Todo.objects.due_in_seven().filter(todolist__users=request.user)
					todos.extend(taskslist)
				else:
					todolist = get_object_or_404(TodoList, slug=slug)
					todos.extend(todolist.todo_set.all())
				response_data = []
				for todo in todos:
					list_slug = todo.todolist.slug
					list_title = todo.todolist.title
					append_this = {}
					append_this[list_slug] = {}
					append_this[list_slug]['list'] = {}
					append_this[list_slug]['list'][todo.slug] = {}
					append_this[list_slug]['list_title'] = list_title
					append_this[list_slug]['list'][todo.slug]['title'] = todo.title
					append_this[list_slug]['list'][todo.slug]['has_description'] = todo.has_description()
					try:
						overdue, due_date, status = todo.get_due_date()
						append_this[list_slug]['list'][todo.slug]['due_date'] = {}
						append_this[list_slug]['list'][todo.slug]['due_date']['overdue'] = overdue
						append_this[list_slug]['list'][todo.slug]['due_date']['date'] = due_date
						append_this[list_slug]['list'][todo.slug]['due_date']['status'] = status
					except:
						pass

					append_this[list_slug]['list'][todo.slug]['edit_url'] = reverse('task_edit', kwargs={'task_slug': todo.slug})
					append_this[list_slug]['list'][todo.slug]['done_url'] = reverse('task_done', kwargs={'task_slug': todo.slug})
					append_this[list_slug]['list'][todo.slug]['archive_url'] = reverse('task_archive', kwargs={'task_slug': todo.slug})
					response_data.append(append_this)
				json_data = json.dumps(response_data)
		return HttpResponse(json_data, content_type='application/json')
	raise Http404











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

	users = todolist.users.exclude(id=todolist.creator.id)
	todolistForm = EditListForm(request.POST or None, initial={'title':todolist.title})
	add_user_form = AddUserToListForm(request.POST or None)
	if request.method == 'POST':
		submit = request.POST.get('submit')
		print submit
		if todolistForm.is_valid() and submit == 'Save Title' and request.POST.get('username') == '' :
			todolist.title = todolistForm.cleaned_data['title']
			todolist.save()
			return HttpResponseRedirect(request.get_full_path())
		elif (add_user_form.is_valid() and submit == 'Add User') or (add_user_form.is_valid() and request.POST.get('username') != ''):
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


@login_required
def list_delete_user(request,list_slug,id):
	todolist = get_object_or_404(TodoList, slug=list_slug)
	if request.user not in todolist.users.all():
		raise Http404
	user = todolist.users.get(id=id)
	todolist.users.remove(user)
	if request.user == user:
		return redirect('home')	
	return redirect('list_edit', list_slug=list_slug)


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

