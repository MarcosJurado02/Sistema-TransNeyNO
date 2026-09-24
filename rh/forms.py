from django import forms

from core.models import Empleado, JefeDirecto, Puesto, Sucursal, TipoEmpleado


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = (
            'numero_empleado',
            'nombre',
            'tipo_empleado',
            'sucursal',
            'puesto',
            'fecha_alta',
            'jefe_directo',
        )
        widgets = {
            'fecha_alta': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_empleado'].queryset = TipoEmpleado.objects.filter(activo=True).order_by('nombre')
        self.fields['tipo_empleado'].empty_label = 'Selecciona una opción'
        self.fields['sucursal'].queryset = Sucursal.objects.filter(activa=True).order_by('nombre')
        self.fields['sucursal'].empty_label = 'Selecciona una opción'
        self.fields['puesto'].widget = forms.Select(
            choices=[('', 'Selecciona una opción')] + list(
                Puesto.objects.filter(activo=True).order_by('nombre').values_list('nombre', 'nombre')
            ),
        )
        self.fields['jefe_directo'].queryset = JefeDirecto.objects.filter(activo=True).order_by('nombre')
        self.fields['jefe_directo'].empty_label = 'Selecciona una opción'
        self.fields['numero_empleado'].required = False
        self.fields['tipo_empleado'].required = False
        self.fields['sucursal'].required = False
        self.fields['puesto'].required = False
        self.fields['fecha_alta'].required = False
        self.fields['jefe_directo'].required = False

    def clean_numero_empleado(self):
        value = self.cleaned_data.get('numero_empleado')
        return value.strip() if value else None
