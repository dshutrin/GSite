from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
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
	
	def to_json(self):
		return {
			'id': self.id,
			'user': {'id': self.user.id, 'username': self.user.username},
			'title': self.title,
			'likes': self.likes,
			'privacy_mode': self.privacy_mode,
			'category': self.category.name,
			'color': self.category.color
		}
	
	def __str__(self):
		return f'{self.title} ({self.user.username})'


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
	title = models.CharField(max_length=150, null=False, verbose_name='Название статьи')
	likes = models.IntegerField(verbose_name='Звёзды', default=0)
	category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, default=None, null=True)
	create_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
	post_file = models.FileField(verbose_name='Файл статьи', upload_to=get_upload_path, validators=[FileExtensionValidator(allowed_extensions=["html"])])
	
	def __str__(self):
		return f'Статья: {self.title}'
