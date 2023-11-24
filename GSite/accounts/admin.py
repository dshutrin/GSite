from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Project)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'likes', 'privacy_mode')