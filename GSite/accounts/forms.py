from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import *


class BeautyForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control bg-light text-dark'
			visible.field.widget.attrs['placeholder'] = visible.field.label


class LoginForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control bg-light text-dark'
			visible.field.widget.attrs['placeholder'] = visible.field.label

	username = forms.CharField(max_length=255, label='Имя пользователя')
	password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')


class RegisterForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control bg-light text-dark'
			visible.field.widget.attrs['placeholder'] = visible.field.label

	username = forms.CharField(label='Имя пользователя', min_length=5, max_length=150)
	first_name = forms.CharField(label='Имя', max_length=255, required=True)
	last_name = forms.CharField(label='Фамилия', max_length=255, required=True)
	email = forms.EmailField(label='email')
	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

	def username_clean(self):
		username = self.cleaned_data['username'].lower()
		new = get_user_model().objects.filter(username=username)
		if new.count():
			raise ValidationError("User Already Exists")
		return username

	def email_clean(self):
		email = self.cleaned_data['email'].lower()
		new = get_user_model().objects.filter(email=email)
		if new.count():
			raise ValidationError("Email Already Exists")
		return email

	def clean_password2(self):
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']

		if password1 and password2 and password1 != password2:
			raise ValidationError("Password don't match")
		return password2

	def save(self, commit=True):
		user = get_user_model().objects.create_user(
			self.cleaned_data['username'],
			self.cleaned_data['email'],
			self.cleaned_data['password1']
		)
		return user

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')


class CreateProjectForm(BeautyForm):
	privacy_mode = forms.ChoiceField(label='Приватность', choices=((True, "Публичный"), (False, "Приватный")))
	category = forms.ModelChoiceField(label='Категория', queryset=ProjectCategory.objects.all())
	
	class Meta:
		model = Project
		fields = ('title', 'privacy_mode', 'category')


class CreatePostForm(BeautyForm):
	category = forms.ModelChoiceField(label='Категория', queryset=ProjectCategory.objects.all())
	
	class Meta:
		model = Post
		fields = ('title', 'category', 'post_file')


class ProfileForm(BeautyForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')


class AddProjectFileForm(BeautyForm):
	class Meta:
		model = ProjectFile
		fields = ('file', 'name')


class ChangeAvatarForm(BeautyForm):
	class Meta:
		model = Profile
		fields = ('avatar', )


class ChangeBannerForm(BeautyForm):
	class Meta:
		model = Profile
		fields = ('banner',)
