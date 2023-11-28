from django import forms


class MainSearchForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control bg-light text-dark p-2 m-0'
			visible.field.widget.attrs['placeholder'] = visible.field.label
			visible.field.widget.attrs['oninput'] = 'get_projects()'
	
	content = forms.CharField(label='Поиск', max_length='256')
