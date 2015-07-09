from django.contrib import admin
from .models import Todo, TodoList

# Register your models here.

class TodoInline(admin.TabularInline):
	model = Todo


class TodoAdmin(admin.ModelAdmin):
	list_filter = ('todolist', 'status')
	list_display = ('__unicode__', 'todolist', 'due_date', 'order', 'status')


class TodoListAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'updated', 'status')

admin.site.register(Todo,TodoAdmin)
admin.site.register(TodoList, TodoListAdmin)