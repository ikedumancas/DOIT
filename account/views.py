from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegisterForm

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
		User.objects.create_user(username=username, email=email, password=password)
		return redirect('login')
	context = {
		'form':form,
	}
	template = "account/register_form.html"
	return render(request, template, context)