
from django import forms

from .models import Todo


class ListReorderForm(forms.Form):
	order = forms.IntegerField(min_value=1)
	task_slug = forms.CharField(max_length=15)


class ListForm(forms.Form):
	title = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'New List Title','id':'create_quick_list'}),
		label = '',
		help_text="Press [Enter] to create"
		)

class TaskForm(forms.Form):
	title = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'New Task', 'class':'create_quick_task'}),
		label = ''
		)
	todolist = forms.CharField();

class FullTodoForm(forms.ModelForm):
	due_date = forms.DateField(
		help_text = 'Format: YYYY-MM-DD',
		required = False
		)
	subscribe_user = forms.BooleanField(
		help_text='Note: Check this field if you want to be notified when other users make changes on this task.',
		label='Subscribe',
		required=False
		)
	class Meta:
		model = Todo
		fields = ['todolist','title', 'description', 'order', 'status', 'due_date', 'subscribe_user']
		labels = {
			'todolist':'List'
		}
"""
NoListFullTodoForm is used when the user is not the creator of the list.
This form will not allow other users to transfer Tasks to other TodoList.
*There might be a better way to do this.
"""
class NoListFullTodoForm(FullTodoForm):
	class Meta:
		model = Todo
		fields = ['title', 'description', 'order', 'status', 'due_date', 'subscribe_user']