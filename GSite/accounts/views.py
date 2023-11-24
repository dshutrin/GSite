from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import login as user_login, logout as user_logout, authenticate
from .forms import *
from .models import *


# Create your views here.
def login(request):
	if request.method == 'GET':
		return render(request, 'accounts/login_page.html', {'form': LoginForm()})
	elif request.method == 'POST':
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)
		if user is not None:
			user_login(request, user)
			return HttpResponseRedirect('/')
		else:
			return render(request, 'accounts/login_page.html', {
				'form': LoginForm(request.POST)
			})


def logout(request):
	user_logout(request)
	return HttpResponseRedirect('/')


def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.save()
			user_login(request, user)
			return HttpResponseRedirect('/')
		else:
			return render(request, 'accounts/register_page.html', {'form': form})
	elif request.method == 'GET':
		return render(request, 'accounts/register_page.html', {'form': RegisterForm()})


def account(request):
	return render(request, 'accounts/profile.html', {
		'projects': Project.objects.filter(user=request.user)
	})


def create_project(request):
	if request.method == 'GET':
		return render(request, 'accounts/create_project.html', {'form': CreateProjectForm()})
	elif request.method == 'POST':
		form = CreateProjectForm(request.POST)
		if form.is_valid():
			Project.objects.create(
				user=request.user,
				likes=0,
				title=request.POST['title'],
				privacy_mode={'True': True, 'False': False}[request.POST['privacy_mode']]
			)
			return HttpResponseRedirect('/accounts')
		else:
			return render(request, 'accounts/create_project.html', {'form': form})


def project_detail(request, project_id):
	project = Project.objects.filter(id=project_id)
	if len(project):
		
		project = project[0]
		return render(request, 'accounts/project_detail.html', {
			'project': project
		})
		
	else:
		return HttpResponseRedirect('/accounts')
