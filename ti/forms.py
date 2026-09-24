from django import forms

from core.models import Sucursal

from .models import Impresora


class ImpresoraForm(forms.ModelForm):
	required_fields = ('sucursal', 'ubicacion', 'marca', 'modelo', 'numero_serie')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['sucursal'] = forms.ChoiceField(
			choices=[('', 'Selecciona una sucursal')] + [(s.nombre, s.nombre) for s in Sucursal.objects.filter(activa=True)],
		)
		self.fields['marca'] = forms.ChoiceField(
			choices=[('', 'Selecciona una marca')] + [(brand.title(), brand.title()) for brand in ('kyocera', 'epson', 'hp', 'brother', 'ricoh')],
		)
		for field_name in self.required_fields:
			self.fields[field_name].required = True
		self.fields['usuario'].widget.attrs['autocomplete'] = 'off'
		self.fields['contrasena'].widget.attrs['autocomplete'] = 'new-password'

	def save(self, commit=True):
		instance = super().save(commit=False)
		for field_name in self.Meta.fields:
			if field_name not in self.required_fields and not getattr(instance, field_name):
				setattr(instance, field_name, 'No aplica')
		if commit:
			instance.save()
		return instance

	class Meta:
		model = Impresora
		fields = (
			'sucursal', 'ubicacion', 'marca', 'modelo', 'numero_serie', 'mac', 'ip',
			'usuario', 'contrasena', 'estatus', 'toner', 'proveedor',
			'nombre_proveedor', 'numero_a_reportar',
		)
		widgets = {
			'usuario': forms.TextInput(attrs={'autocomplete': 'off'}),
			'contrasena': forms.PasswordInput(render_value=True, attrs={'autocomplete': 'new-password'}),
		}