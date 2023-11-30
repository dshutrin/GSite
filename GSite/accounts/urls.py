from django.urls import path
from .views import *


urlpatterns = [
	path('', account),
	path('login', login),
	path('logout', logout),
	path('register', register),
	path('create_project', create_project),
	path('projects/<int:project_id>', project_detail),
	path('get_projects/<str:query>', search_projects),
	path('get_diagram_data', get_diagram_data),
	path('create_post', create_post),
	path('posts/<int:post_id>', post_detail),
	path('settings', settings_profile),
	path('change_avatar', change_avatar),
	path('change_banner', change_banner)
]
