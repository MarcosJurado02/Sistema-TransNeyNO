from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError
from django.shortcuts import redirect, render

from core.models import Departamento, JefeDirecto, Puesto, Sucursal, TipoEmpleado

from .forms import DepartamentoForm, JefeDirectoForm, PuestoForm, SucursalForm, TipoEmpleadoForm


def can_access_catalogs(user):
	if not user.is_authenticated:
		return False
	if user.is_superuser or user.is_staff:
		return True
	return user.groups.filter(name__in=('Admin', 'Administradores', 'RH', 'Recursos Humanos', 'TI', 'Inventario TI')).exists()


def require_catalog_access(user):
	if not can_access_catalogs(user):
		raise PermissionDenied


@login_required
def catalogs(request):
	require_catalog_access(request.user)
	sections = [
		{'title': 'Sucursales', 'description': 'Ubicaciones de la empresa', 'url_name': 'catalogos:branches', 'icon': 'sucursal'},
		{'title': 'Departamentos', 'description': 'Áreas de trabajo', 'url_name': 'catalogos:departments', 'icon': 'departamento'},
		{'title': 'Puestos', 'description': 'Puestos disponibles', 'url_name': 'catalogos:positions', 'icon': 'puesto'},
		{'title': 'Tipos de empleado', 'description': 'Clasificación del personal', 'url_name': 'catalogos:employee-types', 'icon': 'tipo-empleado'},
		{'title': 'Jefes directos', 'description': 'Opciones para asignar al personal', 'url_name': 'catalogos:direct-bosses', 'icon': 'jefe-directo'},
	]
	return render(request, 'catalogos/home.html', {'sections': sections})


def catalog_items(queryset):
	return [
		{'object': item, 'active': getattr(item, 'activa', getattr(item, 'activo', False))}
		for item in queryset
	]


def catalog_form(request, form_class, model, title, heading, item_label, instance=None, success_url=None):
	form = form_class(request.POST or None, instance=instance)
	if request.method == 'POST' and form.is_valid():
		form.save()
		message = 'Registro actualizado correctamente.' if instance else 'Registro agregado correctamente.'
		messages.success(request, message, extra_tags='catalog-success')
		return redirect(success_url or request.resolver_match.view_name)
	if request.method == 'POST' and form.errors.get('nombre'):
		messages.error(request, 'Ese nombre ya está registrado. Usa un nombre diferente.', extra_tags='catalog-duplicate')
		form.errors.pop('nombre', None)
	return render(request, 'catalogos/form.html', {
		'form': form,
		'title': title,
		'heading': heading,
		'items': catalog_items(model.objects.all()),
		'item_label': item_label,
		'editing': instance is not None,
	})


@login_required
def sucursales(request):
	require_catalog_access(request.user)
	return catalog_form(request, SucursalForm, Sucursal, 'Sucursales', 'Registrar sucursal', 'sucursales')


@login_required
def departamentos(request):
	require_catalog_access(request.user)
	return catalog_form(request, DepartamentoForm, Departamento, 'Departamentos', 'Registrar departamento', 'departamentos')


@login_required
def puestos(request):
	require_catalog_access(request.user)
	return catalog_form(request, PuestoForm, Puesto, 'Puestos', 'Registrar puesto', 'puestos')


@login_required
def tipos_empleado(request):
	require_catalog_access(request.user)
	return catalog_form(request, TipoEmpleadoForm, TipoEmpleado, 'Tipos de empleado', 'Registrar tipo de empleado', 'tipos de empleado')


@login_required
def jefes_directos(request):
	require_catalog_access(request.user)
	return catalog_form(request, JefeDirectoForm, JefeDirecto, 'Jefes directos', 'Registrar jefe directo', 'jefes directos')


@login_required
def editar_sucursal(request, pk):
	require_catalog_access(request.user)
	return catalog_form(request, SucursalForm, Sucursal, 'Sucursales', 'Editar sucursal', 'sucursales', Sucursal.objects.get(pk=pk), 'catalogos:branches')


@login_required
def editar_departamento(request, pk):
	require_catalog_access(request.user)
	return catalog_form(request, DepartamentoForm, Departamento, 'Departamentos', 'Editar departamento', 'departamentos', Departamento.objects.get(pk=pk), 'catalogos:departments')


@login_required
def editar_puesto(request, pk):
	require_catalog_access(request.user)
	return catalog_form(request, PuestoForm, Puesto, 'Puestos', 'Editar puesto', 'puestos', Puesto.objects.get(pk=pk), 'catalogos:positions')


@login_required
def editar_tipo_empleado(request, pk):
	require_catalog_access(request.user)
	return catalog_form(request, TipoEmpleadoForm, TipoEmpleado, 'Tipos de empleado', 'Editar tipo de empleado', 'tipos de empleado', TipoEmpleado.objects.get(pk=pk), 'catalogos:employee-types')


@login_required
def editar_jefe_directo(request, pk):
	require_catalog_access(request.user)
	return catalog_form(request, JefeDirectoForm, JefeDirecto, 'Jefes directos', 'Editar jefe directo', 'jefes directos', JefeDirecto.objects.get(pk=pk), 'catalogos:direct-bosses')


def catalog_action(request, model, pk, redirect_name, action):
	require_catalog_access(request.user)
	if request.method != 'POST':
		return redirect(redirect_name)
	item = model.objects.get(pk=pk)
	if action == 'delete':
		try:
			item.delete()
			messages.error(request, 'Registro eliminado correctamente.', extra_tags='catalog-delete')
		except ProtectedError:
			messages.error(request, 'No se puede eliminar porque el registro está en uso.', extra_tags='catalog-error')
	else:
		field = 'activa' if hasattr(item, 'activa') else 'activo'
		setattr(item, field, not getattr(item, field))
		item.save(update_fields=[field])
		if getattr(item, field):
			messages.success(request, 'Registro activado correctamente.', extra_tags='catalog-success')
		else:
			messages.error(request, 'Registro desactivado correctamente.', extra_tags='catalog-deactivate')
	return redirect(redirect_name)


@login_required
def eliminar_sucursal(request, pk):
	return catalog_action(request, Sucursal, pk, 'catalogos:branches', 'delete')


@login_required
def cambiar_estado_sucursal(request, pk):
	return catalog_action(request, Sucursal, pk, 'catalogos:branches', 'toggle')


@login_required
def eliminar_departamento(request, pk):
	return catalog_action(request, Departamento, pk, 'catalogos:departments', 'delete')


@login_required
def cambiar_estado_departamento(request, pk):
	return catalog_action(request, Departamento, pk, 'catalogos:departments', 'toggle')


@login_required
def eliminar_puesto(request, pk):
	return catalog_action(request, Puesto, pk, 'catalogos:positions', 'delete')


@login_required
def cambiar_estado_puesto(request, pk):
	return catalog_action(request, Puesto, pk, 'catalogos:positions', 'toggle')


@login_required
def eliminar_tipo_empleado(request, pk):
	return catalog_action(request, TipoEmpleado, pk, 'catalogos:employee-types', 'delete')


@login_required
def cambiar_estado_tipo_empleado(request, pk):
	return catalog_action(request, TipoEmpleado, pk, 'catalogos:employee-types', 'toggle')


@login_required
def eliminar_jefe_directo(request, pk):
	return catalog_action(request, JefeDirecto, pk, 'catalogos:direct-bosses', 'delete')


@login_required
def cambiar_estado_jefe_directo(request, pk):
	return catalog_action(request, JefeDirecto, pk, 'catalogos:direct-bosses', 'toggle')