from random import randint as rd
import os


def get_cat_color():
	return f'#{rd(1, 9)}{rd(0, 9)}{rd(0, 9)}{rd(0, 9)}{rd(0, 9)}{rd(0, 9)}'


def get_upload_path(instance, filename):
	return os.path.join("user_%d" % instance.user.id, "posts", filename)
