from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from core.models import Empleado, JefeDirecto, Puesto, Sucursal

from .forms import EmpleadoForm


def can_access_hr(user):
	if not user.is_authenticated:
		return False
	if user.is_superuser or user.is_staff:
		return True
	return user.groups.filter(name__in=('Admin', 'Administradores', 'RH', 'Recursos Humanos')).exists()


@login_required
def employees(request):
	if not can_access_hr(request.user):
		raise PermissionDenied

	sections = [
		{
			'anchor': 'empleados',
			'icon': 'personas',
			'title': 'Empleados',
			'description': 'Personal registrado',
			'url': 'rh:employee-list',
		},
		{
			'anchor': 'alta-empleado',
			'icon': 'alta',
			'title': 'Alta de empleado',
			'description': 'Registrar personal nuevo',
			'url': 'rh:employee-create',
		},
	]
	return render(request, 'rh/employees.html', {
		'sections': sections,
	})


@login_required
def employee_list(request):
	if not can_access_hr(request.user):
		raise PermissionDenied

	active_tab = request.GET.get('tab', 'active')
	empleados_query = Empleado.objects.select_related('tipo_empleado', 'sucursal', 'jefe_directo').filter(activo=active_tab != 'inactive')
	sucursal_id = request.GET.get('sucursal')
	jefe_id = request.GET.get('jefe')
	puesto = request.GET.get('puesto', '').strip()
	nombre = request.GET.get('nombre', '').strip()
	if sucursal_id:
		empleados_query = empleados_query.filter(sucursal_id=sucursal_id)
	if jefe_id:
		empleados_query = empleados_query.filter(jefe_directo_id=jefe_id)
	if puesto:
		empleados_query = empleados_query.filter(puesto=puesto)
	if nombre:
		empleados_query = empleados_query.filter(Q(nombre__icontains=nombre) | Q(numero_empleado__icontains=nombre))
	empleados = list(empleados_query)
	empleados.sort(
		key=lambda empleado: (
			empleado.numero_empleado in (None, ''),
			int(empleado.numero_empleado) if empleado.numero_empleado and empleado.numero_empleado.isdigit() else 0,
			empleado.nombre.casefold(),
		)
	)
	paginator = Paginator(empleados, 25)
	page_obj = paginator.get_page(request.GET.get('page'))
	filter_query = request.GET.copy()
	filter_query.pop('page', None)
	return render(request, 'rh/employee_list.html', {
		'empleados': page_obj,
		'page_obj': page_obj,
		'total_empleados': paginator.count,
		'active_tab': active_tab,
		'sucursales': Sucursal.objects.filter(activa=True),
		'jefes_directos': JefeDirecto.objects.filter(activo=True),
		'puestos': Puesto.objects.filter(activo=True),
		'current_sucursal': sucursal_id or '',
		'current_jefe': jefe_id or '',
		'current_puesto': puesto,
		'current_nombre': nombre,
		'filter_query': filter_query.urlencode(),
	})


@login_required
def employee_create(request):
	if not can_access_hr(request.user):
		raise PermissionDenied
	form = EmpleadoForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Empleado registrado correctamente.', extra_tags='rh-success')
		return redirect('rh:employee-list')
	return render(request, 'rh/employee_form.html', {'form': form, 'editing': False})


@login_required
def employee_edit(request, pk):
	if not can_access_hr(request.user):
		raise PermissionDenied
	empleado = get_object_or_404(Empleado, pk=pk)
	form = EmpleadoForm(request.POST or None, instance=empleado)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Empleado actualizado correctamente.', extra_tags='rh-success')
		return redirect('rh:employee-list')
	return render(request, 'rh/employee_form.html', {'form': form, 'editing': True, 'empleado': empleado})


@login_required
def employee_retire(request, pk):
	if not can_access_hr(request.user):
		raise PermissionDenied
	if request.method == 'POST':
		empleado = get_object_or_404(Empleado, pk=pk)
		if empleado.activo:
			empleado.activo = False
			empleado.fecha_baja = timezone.localdate()
			empleado.save(update_fields=('activo', 'fecha_baja'))
			messages.success(request, 'Empleado dado de baja correctamente.', extra_tags='rh-success')
	return redirect('rh:employee-list')