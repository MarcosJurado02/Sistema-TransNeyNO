from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from core.models import Sucursal

from .models import Impresora


class InventoryAccessTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='ti-user', password='test-pass')
		self.admin = User.objects.create_user(
			username='admin-user',
			password='test-pass',
			is_staff=True,
		)
		self.ti_group = Group.objects.create(name='TI')
		self.user.groups.add(self.ti_group)
		Sucursal.objects.get_or_create(nombre='Monterrey', defaults={'ciudad': 'Monterrey'})

	def test_ti_user_can_open_inventory(self):
		self.client.force_login(self.user)

		response = self.client.get(reverse('ti:inventory'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Activos de cómputo')
		self.assertContains(response, 'Impresoras')
		self.assertContains(response, 'Redes Wi-Fi')
		self.assertContains(response, 'Líneas telefónicas')

	def test_user_without_ti_access_is_forbidden(self):
		user_without_access = User.objects.create_user(
			username='general-user',
			password='test-pass',
		)
		self.client.force_login(user_without_access)

		response = self.client.get(reverse('ti:inventory'))

		self.assertEqual(response.status_code, 403)

	def test_admin_can_open_inventory(self):
		self.client.force_login(self.admin)

		response = self.client.get(reverse('ti:inventory'))

		self.assertEqual(response.status_code, 200)

	def test_inventory_submodules_only_show_inside_inventory(self):
		self.client.force_login(self.admin)

		response = self.client.get(reverse('core:dashboard'))

		self.assertNotContains(response, 'Activos de cómputo')
		self.assertNotContains(response, 'Redes Wi-Fi')

	def test_rh_menu_only_shows_rh_module(self):
		rh_user = User.objects.create_user(
			username='rh-user',
			password='test-pass',
		)
		rh_user.groups.add(Group.objects.create(name='RH'))
		self.client.force_login(rh_user)

		response = self.client.get(reverse('core:dashboard'))

		self.assertContains(response, 'Recursos humanos')
		self.assertNotContains(response, 'Inventario TI')

	def test_ti_can_open_printer_tabs(self):
		self.client.force_login(self.user)

		active_response = self.client.get(reverse('ti:printers'))
		inactive_response = self.client.get(reverse('ti:printers') + '?tab=inactive')

		self.assertEqual(active_response.status_code, 200)
		self.assertContains(active_response, 'Activas')
		self.assertContains(active_response, 'Bajas')
		self.assertEqual(inactive_response.status_code, 200)

	def test_ti_can_register_printer(self):
		self.client.force_login(self.user)

		response = self.client.post(reverse('ti:register-printer'), {
			'sucursal': 'Monterrey',
			'ubicacion': 'Oficina principal',
			'marca': 'Brother',
			'modelo': 'DCP-L5650DN',
			'numero_serie': 'U64197',
			'mac': 'B4-22-00-7E-95-71',
			'ip': '192.168.100.151',
		})

		self.assertRedirects(response, reverse('ti:printers'))

	def test_printer_requires_identification_fields(self):
		self.client.force_login(self.user)

		response = self.client.post(reverse('ti:register-printer'), {})

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['form'].errors)
		self.assertIn('sucursal', response.context['form'].errors)
		self.assertEqual(Impresora.objects.count(), 0)

	def test_ti_can_edit_and_retire_printer(self):
		printer = Impresora.objects.create(
			sucursal='Monterrey', ubicacion='Oficina', marca='Brother',
			modelo='DCP', numero_serie='SER-001',
		)
		self.client.force_login(self.user)

		response = self.client.post(reverse('ti:edit-printer', args=[printer.pk]), {
			'sucursal': 'Monterrey', 'ubicacion': 'Oficina nueva', 'marca': 'Brother',
			'modelo': 'DCP', 'numero_serie': 'SER-001', 'mac': '', 'ip': '',
			'usuario': '', 'contrasena': '', 'estatus': '', 'toner': '',
			'proveedor': '', 'nombre_proveedor': '', 'numero_a_reportar': '',
		})

		self.assertRedirects(response, reverse('ti:printers'))
		response = self.client.post(reverse('ti:retire-printer', args=[printer.pk]), {'motivo_baja': 'Equipo reemplazado'})
		self.assertRedirects(response, reverse('ti:printers'))
		printer.refresh_from_db()
		self.assertFalse(printer.activa)
		self.assertEqual(printer.motivo_baja, 'Equipo reemplazado')

	def test_retirement_requires_reason(self):
		printer = Impresora.objects.create(
			sucursal='Monterrey', ubicacion='Oficina', marca='Brother',
			modelo='DCP', numero_serie='SER-002',
		)
		self.client.force_login(self.user)

		response = self.client.post(reverse('ti:retire-printer', args=[printer.pk]), {})

		self.assertRedirects(response, reverse('ti:printers'))
		printer.refresh_from_db()
		self.assertTrue(printer.activa)
