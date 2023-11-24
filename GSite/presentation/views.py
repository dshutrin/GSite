from django.shortcuts import render
from accounts.models import Project
from django.contrib.auth.models import User


# Create your views here.
def home(request):
	return render(request, 'presentation/home.html', {
		'projects_count': Project.objects.all().count(),
		'users_count': User.objects.all().count(),
		'most_liked': Project.objects.filter(privacy_mode=True).order_by('-likes')[:10]
	})
