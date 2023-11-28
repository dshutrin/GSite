from django.shortcuts import render
from accounts.models import *
from .forms import *


# Create your views here.
def home(request):
	form = MainSearchForm()
	if request.method == 'POST':
		form = MainSearchForm(request.POST)
		
	return render(request, 'presentation/home.html', {
		'most_liked': Project.objects.filter(privacy_mode=True).order_by('-likes')[:6],
		'form': form
	})
