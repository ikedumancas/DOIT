from django import forms

from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(label="Username",widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class RegisterForm(forms.Form):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'youremail@provider.com'}))
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if len(password1) < 5:
			raise forms.ValidationError("Password is too short")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def clean_username(self):
		username = self.cleaned_data.get('username')
		try:
			exists = User.objects.get(username=username)
			if exists:
				raise forms.ValidationError("This usernam is taken")
		except User.DoesNotExist:
			return username
		except:
			raise forms.ValidationError("There was an error, please try again or contact us.")

	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			exists = User.objects.get(email=email)
			raise forms.ValidationError("This email is taken")
		except User.DoesNotExist:
			return email
		except:
			raise forms.ValidationError("There was an error, please try again or contact us.")