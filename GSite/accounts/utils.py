from random import randint as rd


def get_cat_color():
	return f'#{rd(1, 9)}{rd(0, 9)}{rd(0, 9)}{rd(0, 9)}{rd(0, 9)}{rd(0, 9)}'
