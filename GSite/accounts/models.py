import os

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .utils import *

from django.conf import settings
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver


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
	
	def get_privacy(self):
		return {True: 'Публичный', False: 'Приватный'}[self.privacy_mode]
	
	def __str__(self):
		return f'{self.title} ({self.user.username})'


class ProjectFile(models.Model):
	project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.CASCADE)
	name = models.CharField(max_length=255, verbose_name='Название файла', default='')
	file = models.FileField(upload_to=get_projects_files_path, verbose_name='Файл проекта')


class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
	title = models.CharField(max_length=150, null=False, verbose_name='Название статьи')
	likes = models.IntegerField(verbose_name='Звёзды', default=0)
	category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, default=None, null=True)
	create_date = models.DateTimeField(verbose_name='Дата публикации', auto_now_add=True)
	post_file = models.FileField(verbose_name='Файл статьи', upload_to=get_upload_path, validators=[FileExtensionValidator(allowed_extensions=["html"])])
	
	def __str__(self):
		return f'Статья: {self.title}'


class Profile(models.Model):
	user = models.OneToOneField(User, verbose_name='Пользователь', on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to=get_avatar_path, verbose_name='Аватар', default=None, null=True)
	banner = models.ImageField(upload_to=get_banner_path, verbose_name='Баннер', default=None, null=True)
	
	def __str__(self):
		avatar = self.avatar if self.avatar else False
		banner = self.banner if self.banner else False
		return f'AVATAR: {avatar}\nBANNER: {banner}'


@receiver(post_delete, sender=ProjectFile)
def delete_project_files(sender, instance, **kwargs):
	if os.path.exists(os.path.join(settings.BASE_DIR, instance.file.path)):
		os.remove(os.path.join(settings.BASE_DIR, instance.file.path))
		

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		profile = Profile.objects.create(user=instance)
		instance.profile = profile
		instance.save()
		
		
@receiver(pre_save, sender=Profile)
def manage_photos(sender, instance, **kwargs):
	try:
		profile = Profile.objects.get(id=instance.id)
		if profile.banner != instance.banner:
			os.remove(profile.banner.path)
		if profile.avatar != instance.avatar:
			os.remove(profile.avatar.path)
	except:
		pass
