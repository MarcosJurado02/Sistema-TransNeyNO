from django import forms

from core.models import Departamento, JefeDirecto, Puesto, Sucursal, TipoEmpleado


class SucursalForm(forms.ModelForm):
	class Meta:
		model = Sucursal
		fields = ('nombre', 'ciudad', 'direccion', 'activa')


class DepartamentoForm(forms.ModelForm):
	class Meta:
		model = Departamento
		fields = ('nombre', 'descripcion', 'activo')


class PuestoForm(forms.ModelForm):
	class Meta:
		model = Puesto
		fields = ('nombre', 'descripcion', 'activo')


class TipoEmpleadoForm(forms.ModelForm):
	class Meta:
		model = TipoEmpleado
		fields = ('nombre', 'descripcion', 'activo')


class JefeDirectoForm(forms.ModelForm):
	class Meta:
		model = JefeDirecto
		fields = ('nombre', 'activo')