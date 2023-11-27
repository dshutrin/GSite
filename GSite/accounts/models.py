from django.db import models
from django.contrib.auth.models import User
from .utils import *


# Create your models here.
class ProjectCategory(models.Model):
	name = models.CharField(max_length=150, null=False, default=None)
	color = models.CharField(max_length=20, null=True, default=get_cat_color)
	
	def __str__(self):
		return f'Категория: {self.name}'


class Project(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
	title = models.CharField(max_length=150, null=False, verbose_name='Название проекта')
	likes = models.IntegerField(verbose_name='Звёзды', default=0)
	privacy_mode = models.BooleanField(default=True, verbose_name='Приватность')
	category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, default=None, null=True)
	
	def __str__(self):
		return f'{self.title} ({self.user.username})'
