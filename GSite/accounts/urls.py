from django.urls import path
from .views import *


urlpatterns = [
	path('', account),
	path('login', login),
	path('logout', logout),
	path('register', register),
	path('create_project', create_project),
	path('projects/<int:project_id>', project_detail)
]
