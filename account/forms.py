from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions


class LoginForm(forms.Form):
	username = forms.CharField(
	    label="Username", widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(
	    widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class RegisterForm(forms.Form):
	first_name = forms.CharField(
	    widget=forms.TextInput(attrs={'placeholder': 'First Name', 'required': 'true' }))
	last_name = forms.CharField(
	    widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'required': 'true'}))
	username = forms.CharField(
	    widget=forms.TextInput(attrs={'placeholder': 'Username', 'required': 'true'}))
	email = forms.EmailField(
	    widget=forms.TextInput(attrs={'placeholder': 'youremail@provider.com', 'required': 'true'}))
	password1 = forms.CharField(
	    label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'required': 'true'}))
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(
	    attrs={'placeholder': 'Password Confirmation', 'required': 'true'}))

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1:
			if len(password2) < 5:
				raise forms.ValidationError("Password is too short")
			if password1 and password2 and password1 != password2:
				raise forms.ValidationError("Passwords don't match")
			return password2
		raise forms.ValidationError("Password error!")

	def clean_username(self):
		username = self.cleaned_data.get('username')
		try:
			exists = User.objects.get(username=username)
			if exists:
				raise forms.ValidationError("This usernam is taken")
		except User.DoesNotExist:
			return username
		except:
			raise forms.ValidationError(
			    "There was an error, please try again or contact us.")

	def clean_email(self):
		email = self.cleaned_data.get('email')
		exists = None
		try:
			exists = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		except:
			raise forms.ValidationError(
			    "There was an error, please try again or contact us.")
		if exists:
			raise forms.ValidationError("This email is taken")


class EditAccountForm(forms.Form):
	first_name = forms.CharField(
		required=False,
		widget=forms.TextInput(
			attrs={'placeholder': 'First Name'}))
	last_name = forms.CharField(
		required=False,
		widget=forms.TextInput(
			attrs={'placeholder': 'Last Name'}))
	bio = forms.CharField(
		required=False,
		widget=forms.Textarea(
			attrs={'placeholder': 'Tell us something about yourself.', 'rows': '4'}))
	facebook = forms.URLField(
		required=False,
		widget=forms.TextInput(
			attrs={'placeholder': 'Facebook profile URL'}))
	twitter = forms.CharField(
		required=False,
		widget=forms.TextInput(
			attrs={'placeholder': 'Twitter handle'}))

	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.label_class = 'col-sm-2'
	helper.field_class = 'col-sm-10'
	helper.layout = Layout(
		'first_name', 'last_name', 'bio', 'facebook', 'twitter',
		FormActions(
			Submit('save_changes', 'Save changes', css_class="btn-primary pull-right"),
		)
	)


class PasswordChangeCrispyForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(PasswordChangeCrispyForm, self).__init__(*args, **kwargs)

	old_password = forms.CharField(
		required=True,
		widget=forms.PasswordInput)
	new_password1 = forms.CharField(
		required=True,
		widget=forms.PasswordInput)
	new_password2 = forms.CharField(
		required=True,
		label='New Password Confirmation',
		widget=forms.PasswordInput)

	def clean_old_password(self):
		old_password = self.cleaned_data["old_password"]
		if not self.user.check_password(old_password):
			raise forms.ValidationError("Your old password was entered incorrectly.")
		return old_password

	helper = FormHelper()
	helper.form_class = 'form-horizontal'
	helper.label_class ='col-sm-2'
	helper.field_class ='col-sm-10'
	helper.layout = Layout(
		'old_password', 'new_password1', 'new_password2',
		FormActions(
			Submit('save_password', 'Save new password', css_class="btn-primary pull-right"),
		)
	)

	def clean_new_password2(self):
        # Check that the two password entries match
		new_password1 = self.cleaned_data.get("new_password1")
		new_password2 = self.cleaned_data.get("new_password2")
		if len(new_password1) < 5:
			raise forms.ValidationError("Password is too short")
		if new_password1 and new_password2 and new_password1 != new_password2:
			raise forms.ValidationError("Passwords don't match")
		return new_password2

class PasswordResetForm(forms.Form):
	email = forms.EmailField(label="Email", required=True)

	def clean_email(self):
		value = self.cleaned_data["email"]
		if not User.objects.filter(email__iexact=value).exists():
			raise forms.ValidationError("Email address can not be found.")
		return value