
from django import forms
from django.contrib.auth.models import User

from .models import Todo


class EditTaskForm(forms.ModelForm):
	due_date = forms.DateField(
		help_text = 'Format: YYYY-MM-DD',
		required = False
		)
	class Meta:
		model = Todo
		fields = ['title', 'description', 'priority', 'order', 'status', 'due_date']
		labels = {
			'todolist':'List'
		}


class ListReorderForm(forms.Form):
	order = forms.IntegerField(min_value=1)
	task_slug = forms.CharField(max_length=15)


class ListForm(forms.Form):
	title = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'New List Title','id':'create_quick_list'}),
		label = '',
		help_text="Press [Enter] to create"
		)

class ListSlugForm(forms.Form):
	slug = forms.CharField(max_length=10)

class EditListForm(forms.Form):
	title = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'List Title','id':'list_title'}),
		label = '',
		)

class AddUserToListForm(forms.Form):
	username = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'Type in Username of the User you want to add.','id':'add_user_to_list'}),
		label = '',
		required = False
		)
	
	def clean_username(self):
		username = self.cleaned_data.get('username')
		if username == '':
			return False

		try:
			user = User.objects.get(username=username)
			return user
		except User.DoesNotExist:
			raise forms.ValidationError("This username does not exist. Please input an existing username.")
		except:
			raise forms.ValidationError(
			    "There was an error, please try again or contact us.")

class TaskForm(forms.Form):
	title = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'New Task', 'class':'create_quick_task', 'id':''}),
		label = ''
		)
	todolist = forms.CharField();

class FullTodoForm(forms.ModelForm):
	due_date = forms.DateField(
		help_text = 'Format: YYYY-MM-DD',
		required = False
		)
	class Meta:
		model = Todo
		fields = ['todolist','title', 'description', 'priority', 'order', 'status', 'due_date']
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
		fields = ['title', 'description', 'order', 'status', 'due_date']