from random import randint as rd
import os


def get_cat_color():
	return f'#{rd(1, 9)}{rd(0, 9)}{rd(0, 9)}{rd(0, 9)}{rd(0, 9)}{rd(0, 9)}'


def get_upload_path(instance, filename):
	return os.path.join("user_%d" % instance.user.id, "posts", filename)


def get_avatar_path(instance, filename):
	return os.path.join("user_%d" % instance.user.id, "avatars", filename)


def get_banner_path(instance, filename):
	return os.path.join("user_%d" % instance.user.id, "banners", filename)


def get_avatar(user):
	if user.profile.avatar:
		return f'/media/{user.profile.avatar}'
	return ''


def get_banner(user):
	if user.profile.banner:
		return f'/media/{user.profile.banner}'
	return ''
