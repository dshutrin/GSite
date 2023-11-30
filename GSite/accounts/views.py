from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
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
		'projects': Project.objects.filter(user=request.user),
		'posts': Post.objects.filter(user=request.user),
		'banner': get_banner(request.user),
		'avatar': get_avatar(request.user)
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
				category=ProjectCategory.objects.get(id=request.POST['category']),
				privacy_mode={'True': True, 'False': False}[request.POST['privacy_mode']]
			)
			return HttpResponseRedirect('/accounts')
		else:
			return render(request, 'accounts/create_project.html', {'form': form})


def create_post(request):
	if request.method == 'GET':
		return render(request, 'accounts/create_post.html', {'form': CreatePostForm()})
	elif request.method == 'POST':
		form = CreatePostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return HttpResponseRedirect('/accounts/')
		return render(request, 'accounts/create_post.html', {'form': CreatePostForm(request.POST, request.FILES)})


def project_detail(request, project_id):
	project = Project.objects.filter(id=project_id)
	if len(project):
		
		project = project[0]
		return render(request, 'accounts/project_detail.html', {
			'project': project
		})
		
	else:
		return HttpResponseRedirect('/accounts')


def search_projects(request, query):
	projects = [x.to_json() for x in Project.objects.filter(title__startswith=query)][:12]
	if len(projects):
		return JsonResponse({
			'status': 'ok',
			'projects': projects
		})
	else:
		return JsonResponse({
			'status':   'bad',
			'projects': None
		})


def get_diagram_data(request):
	cat_names = [x.name for x in ProjectCategory.objects.all()]
	ans = {}
	
	for cat_name in cat_names:
		count = Project.objects.filter(category__name=cat_name).count()
		color = ProjectCategory.objects.filter(name=cat_name)[0].color
		if count > 0:
			ans.update({
				cat_name: {'count': count, 'color': color}
			})
	
	return JsonResponse(ans)


def post_detail(request, post_id):
	post = Post.objects.filter(id=post_id)
	if len(post):
		post = post[0]
		post_filename = 'user_' + str(post.user.id) + '\\posts\\' + post.post_file.path.split('\\')[-1]
		
		return render(request, 'accounts/post_detail.html', {
			'file_name': post_filename,
			'post': post
		})
	else:
		return HttpResponseRedirect('/')


def settings_profile(request):
	if request.POST:
		form = ProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
	
	return render(request, 'accounts/settings.html', {
		'form': ProfileForm(instance=request.user),
		'banner': get_banner(request.user),
		'avatar': get_avatar(request.user)
	})


def change_avatar(request):
	if request.POST:
		form = ChangeAvatarForm(request.POST, request.FILES, instance=request.user.profile)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/')
		else:
			return render(request, 'accounts/change_avatar.html', {
				'avatar': get_avatar(request.user),
				'form':   form
			})
	return render(request, 'accounts/change_avatar.html', {
		'avatar': get_avatar(request.user),
		'form': ChangeAvatarForm()
	})


def change_banner(request):
	if request.POST:
		form = ChangeBannerForm(request.POST, request.FILES, instance=request.user.profile)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/accounts/')
		else:
			return render(request, 'accounts/change_banner.html', {
				'banner': get_banner(request.user),
				'form':   form
			})
	return render(request, 'accounts/change_banner.html', {
		'banner': get_banner(request.user),
		'form': ChangeAvatarForm()
	})
