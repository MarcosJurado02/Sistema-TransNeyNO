from django.contrib import admin

from .models import Departamento, Empleado, JefeDirecto, Puesto, Sucursal, TipoEmpleado


@admin.register(TipoEmpleado)
class TipoEmpleadoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'activo')
	list_filter = ('activo',)
	search_fields = ('nombre',)


@admin.register(JefeDirecto)
class JefeDirectoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'activo')
	list_filter = ('activo',)
	search_fields = ('nombre',)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'activo')
	list_filter = ('activo',)
	search_fields = ('nombre',)


@admin.register(Puesto)
class PuestoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'activo')
	list_filter = ('activo',)
	search_fields = ('nombre',)


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'ciudad', 'activa')
	list_filter = ('activa',)
	search_fields = ('nombre', 'ciudad')


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'numero_empleado', 'puesto', 'sucursal', 'activo')
	list_filter = ('sucursal', 'activo', 'area')
	search_fields = ('nombre', 'numero_empleado', 'correo_institucional')
	autocomplete_fields = ('jefe_directo', 'sucursal')
