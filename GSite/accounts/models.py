from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Project(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
	title = models.CharField(max_length=150, null=False, verbose_name='Название проекта')
	likes = models.IntegerField(verbose_name='Звёзды', default=0)
	privacy_mode = models.BooleanField(default=True, verbose_name='Приватность')
	
	def __str__(self):
		return f'{self.title} ({self.user.username})'
