from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponseRedirect as redirect_to, render, redirect

from .forms import EditAccountForm, LoginForm, RegisterForm, PasswordChangeCrispyForm
from .models import UserProfile

# Create your views here.
def auth_login(request):
	form = LoginForm(request.POST or None)
	next_url = request.GET.get('next')
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username,password=password)
		if user:
			login(request,user)
			if next_url:
				return redirect_to(next_url)	
			return redirect('home')
		else:
			messages.error(request,'Username/Password incorrect.')
	context = {
		'form':form
	}
	template = "account/login.html"
	return render(request, template, context)


@login_required
def auth_logout(request):
	logout(request)
	return redirect('login')


def auth_register(request):
	form = RegisterForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		password = form.cleaned_data['password2']
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']
			
		User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
		return redirect('login')
	context = {
		'form':form,
	}
	template = "account/register_form.html"
	return render(request, template, context)


@login_required
def auth_edit(request):
	user = request.user
	user_data = {
		'first_name':user.first_name, 
		'last_name':user.last_name,
		'bio':user.userprofile.bio,
		'facebook':user.userprofile.facebook,
		'twitter':user.userprofile.twitter
		}
	profileform = EditAccountForm(initial=user_data)
	if request.method == "POST":
		profileform = EditAccountForm(request.POST)
		if not profileform.is_valid():
			messages.error(request, "<strong>Error!</strong> There was an error while saving your data.")
		if profileform.is_valid():
			change_user = User.objects.get(id=request.user.id)
			change_user.first_name = profileform.cleaned_data['first_name']
			change_user.last_name = profileform.cleaned_data['last_name']
			change_user.save()
			change_user_profile = UserProfile.objects.get(id=request.user.userprofile.id)
			change_user_profile.bio = profileform.cleaned_data['bio']
			change_user_profile.facebook = profileform.cleaned_data['facebook']
			change_user_profile.twitter = profileform.cleaned_data['twitter']
			change_user_profile.save()
			messages.success(request, "<strong>Success!</strong> Profile Saved.")
	context = {
		'form':profileform,
	}
	template = "account/edit_account.html"
	return render(request, template, context)


@login_required
def auth_changepassword(request):
	changepasswordform = PasswordChangeCrispyForm(None)
	if request.method == "POST":
		changepasswordform = PasswordChangeCrispyForm(request.POST, user=request.user)
		if changepasswordform.is_valid():
			old_password = changepasswordform.cleaned_data['old_password']
			new_password = changepasswordform.cleaned_data['new_password2']
			if request.user.check_password(old_password):
				u = request.user
				u.set_password(new_password)
				u.save()
				if hasattr(auth, 'update_session_auth_hash'):
					auth.update_session_auth_hash(request, u)
				messages.success(request, "<strong>Success!</strong> Password changed.")
		else:
			messages.error(request, "<strong>Error!</strong> Something went wrong.")
	context = {
		'form':changepasswordform
	}
	template = "account/change_password.html"
	return render(request, template, context)