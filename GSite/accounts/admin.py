from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Project)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('user', 'title', 'likes', 'privacy_mode')


@admin.register(ProjectCategory)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'color')


@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('user', 'title')


@admin.register(ProjectFile)
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('project', 'file')
