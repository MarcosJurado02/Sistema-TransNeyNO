from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ImpresoraForm
from .models import Impresora


def can_access_inventory(user):
	if not user.is_authenticated:
		return False
	if user.is_superuser or user.is_staff:
		return True
	return user.groups.filter(name__in=('Admin', 'Administradores', 'TI', 'Inventario TI')).exists()


@login_required
def inventory(request):
	if not can_access_inventory(request.user):
		raise PermissionDenied

	sections = [
		{
			'anchor': 'activos',
			'icon': '▣',
			'title': 'Activos',
			'description': 'Equipo y periféricos',
		},
		{
			'anchor': 'impresoras',
			'icon': '▤',
			'title': 'Impresoras',
			'description': 'Equipos de impresión',
			'url': 'ti:printers',
		},
		{
			'anchor': 'redes-wifi',
			'icon': '◉',
			'title': 'Redes Wi-Fi',
			'description': 'Conectividad inalámbrica',
		},
		{
			'anchor': 'lineas-telefonicas',
			'icon': '◌',
			'title': 'Telefonía',
			'description': 'Líneas y extensiones',
		},
	]
	return render(request, 'ti/inventory.html', {'sections': sections})


@login_required
def printers(request):
	if not can_access_inventory(request.user):
		raise PermissionDenied

	active_tab = request.GET.get('tab', 'active')
	printers = Impresora.objects.filter(activa=active_tab != 'inactive').order_by('sucursal', 'ubicacion', 'marca', 'modelo')
	return render(request, 'ti/printers.html', {
		'printers': printers,
		'active_tab': active_tab,
		'active_count': Impresora.objects.filter(activa=True).count(),
		'inactive_count': Impresora.objects.filter(activa=False).count(),
	})


@login_required
def register_printer(request):
	if not can_access_inventory(request.user):
		raise PermissionDenied

	form = ImpresoraForm(request.POST if request.method == 'POST' else None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Impresora registrada correctamente.', extra_tags='catalog-success')
		return redirect('ti:printers')
	return render(request, 'ti/printer_form.html', {'form': form, 'editing': False})


@login_required
def edit_printer(request, pk):
	if not can_access_inventory(request.user):
		raise PermissionDenied

	printer = Impresora.objects.get(pk=pk)
	form = ImpresoraForm(request.POST if request.method == 'POST' else None, instance=printer)
	if request.method == 'POST' and form.is_valid():
		form.save()
		messages.success(request, 'Impresora actualizada correctamente.', extra_tags='catalog-success')
		return redirect('ti:printers')
	return render(request, 'ti/printer_form.html', {'form': form, 'editing': True})


@login_required
def retire_printer(request, pk):
	if not can_access_inventory(request.user):
		raise PermissionDenied
	if request.method == 'POST':
		printer = Impresora.objects.get(pk=pk)
		motivo = request.POST.get('motivo_baja', '').strip()
		if not motivo:
			messages.error(request, 'Debes indicar el motivo de la baja.', extra_tags='catalog-error')
			return redirect('ti:printers')
		printer.activa = False
		printer.fecha_baja = timezone.localdate()
		printer.motivo_baja = motivo
		printer.save(update_fields=('activa', 'fecha_baja', 'motivo_baja'))
		messages.error(request, 'Impresora dada de baja correctamente.', extra_tags='catalog-deactivate')
	return redirect('ti:printers')