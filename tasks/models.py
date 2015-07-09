import datetime
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.template.defaultfilters import mark_safe
from django.utils.crypto import get_random_string
# Create your models here.


STATUS_CHOICES = (
	('active', 'Active'),
	('done', 'Done'),
	('archived', 'Archived')
)

class TodoManager(models.Manager):
	def all(self):
		return super(TodoManager,self).exclude(status='archived')

	def create_todo(self, user=None, title=None, list_slug=None):
		if not user:
			raise ValueError('Must include a User when adding a new list')
		if not title:
			raise ValueError('Must include a Title when adding a new list')
		if not list_slug:
			raise ValueError('Task must belong to a list.')

		try:
			todolist = TodoList.objects.get(slug=list_slug)
		except:
			raise ValueError('This does not exist.')

		new_task = self.model(title = title,slug=get_random_string(length=10), todolist=todolist)
		new_task.save(using=self._db)
		
		return new_task

class Todo(models.Model):
	todolist = models.ForeignKey('TodoList', default=1)
	title = models.CharField(max_length=1000)
	order = models.PositiveIntegerField(default=1, blank=True, null=True)
	slug = models.SlugField(max_length=10, blank=True, null=True)
	status = models.SlugField(choices=STATUS_CHOICES, default='active', max_length=10)
	description = models.TextField(max_length=5000, null=True, blank=True)
	due_date  = models.DateField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	objects = TodoManager()

	
	class Meta:
		verbose_name = "Task"
		verbose_name_plural = "Tasks"
		ordering = ['order','timestamp']

	
	def __unicode__(self):
		return self.title


	def change_order_to(self,new):
		old_order = self.order
		new_order = new
		self.order = new_order
		if old_order > new_order:
			tasks_to_change_order = self.todolist.todo_set.filter(
				order__gte = new_order, 
				order__lte = old_order
				).exclude(id=self.id)
			old_order_gte_new_order = True
		elif old_order < new_order:
			tasks_to_change_order = self.todolist.todo_set.filter(
				order__lte = new_order, 
				order__gte = old_order
				).exclude(id=self.id)
			old_order_gte_new_order = False
		for change_order in tasks_to_change_order:
			if old_order_gte_new_order:
				change_order.order = change_order.order + 1
			else:
				change_order.order = change_order.order -1
			change_order.save()
		self.save()

	
	def mark_as_active(self):
		self.status = 'active'
		self.save()

	
	def mark_as_archived(self):
		try:
			tasks_to_change_order = self.todolist.todo_set.filter(
				order__gt = self.order
				)
			for change_order in tasks_to_change_order:
				change_order.order = change_order.order -1
				change_order.save()

		except:
			pass
		self.status = 'archived'
		self.order = None
		self.save()

	
	def mark_as_done(self):
		self.status = 'done'
		self.save()

	
	def due_date_status_badge(self):
		color = 'default'
		overdue = ''
		if self.due_date:
			due_date = self.due_date
			now = datetime.date.today()
			if due_date >= now:
				date_diff = due_date - now
				days_from_due_date = date_diff.days
				if days_from_due_date == 2:
					color = 'info'
					days_from_due_date_string = "%s days" %(days_from_due_date)
				elif days_from_due_date == 1:
					color = 'warning'
					days_from_due_date_string = 'Tomorrow'
				elif days_from_due_date == 0:
					color = 'danger'
					days_from_due_date_string = 'Today'
				else:
					days_from_due_date_string = "%s days" %(days_from_due_date)
			else:
				color = 'danger'
				overdue = 'overdue'
				date_diff = now - due_date
				days_from_due_date = date_diff.days
				if days_from_due_date == 1:
					days_from_due_date_string = "%s day" %(days_from_due_date)
				else:
					days_from_due_date_string = "%s days" %(days_from_due_date)

			return mark_safe('<span class="label label-%s"><span class="glyphicon glyphicon-time" aria-hidden="true"></span> %s %s</span>' %(color, days_from_due_date_string, overdue))
		return ''



class TodoListManager(models.Manager):
	def all(self):
		return super(TodoListManager,self).exclude(status='archived')

	
	def create_list(self, user=None, title=None):
		if not user:
			raise ValueError('Must include a User when adding a new list')
		if not title:
			raise ValueError('Must include a Title when adding a new list')

		new_list = self.model(title = title,slug=get_random_string(length=10))
		new_list.save(using=self._db)
		new_list.users.add(user)
		return new_list


class TodoList(models.Model):
	creator = models.ForeignKey(User, default=1,related_name='created_by')
	users = models.ManyToManyField(User)
	title = models.CharField(max_length=120)
	slug = models.SlugField(max_length=10, blank=True, null=True)
	status = models.SlugField(choices=STATUS_CHOICES, default='active', max_length=10)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	objects = TodoListManager()

	
	class Meta:
		verbose_name = "Todo List"
		verbose_name_plural = "Todo Lists"
		ordering = ['timestamp']


	def __unicode__(self):
		return self.title
	
	def is_created_by(self,user):
		if user == self.creator:
			return True
		return False
	
	def task_count(self):
		return len(self.todo_set.all())

	def mark_as_archived(self):
		self.status = 'archived'
		self.save()



# def updated_todo_list(sender, instance, created, *args, **kwargs):
#     print 
    
# post_save.connect(updated_todo_list, sender=Todo)
def todo_post_save_receiver(sender, instance, created, *args, **kwargs):
	if created:
		new_order_num = len(instance.todolist.todo_set.all()) # The number of task in a list is the new order number
		instance.order = new_order_num
		instance.save()
	instance.todolist.save() # Save the Todolist to change its update datetime.
	# Notify users on the list if an action was made. Except for the user who made the action.
	
post_save.connect(todo_post_save_receiver, sender=Todo)