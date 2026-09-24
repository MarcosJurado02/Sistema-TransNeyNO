from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from core.models import Departamento, Puesto, Sucursal


class CatalogAccessTests(TestCase):
	def setUp(self):
		self.rh_user = User.objects.create_user(username='rh-user', password='test-pass')
		self.rh_user.groups.add(Group.objects.create(name='RH'))
		self.ti_user = User.objects.create_user(username='ti-user', password='test-pass')
		self.ti_user.groups.add(Group.objects.create(name='TI'))
		self.general_user = User.objects.create_user(username='general-user', password='test-pass')

	def test_rh_and_ti_can_open_catalogs(self):
		for user in (self.rh_user, self.ti_user):
			self.client.force_login(user)
			response = self.client.get(reverse('catalogos:home'))
			self.assertEqual(response.status_code, 200)
			self.assertContains(response, 'Sucursales')
			self.assertContains(response, 'Departamentos')
			self.assertContains(response, 'Puestos')

	def test_other_profiles_are_forbidden(self):
		self.client.force_login(self.general_user)

		response = self.client.get(reverse('catalogos:home'))

		self.assertEqual(response.status_code, 403)

	def test_rh_can_register_branch(self):
		self.client.force_login(self.rh_user)

		response = self.client.post(reverse('catalogos:branches'), {
			'nombre': 'Sucursal Norte',
			'ciudad': 'Monterrey',
			'direccion': 'Av. Principal 100',
			'activa': 'on',
		})

		self.assertRedirects(response, reverse('catalogos:branches'))
		self.assertTrue(Sucursal.objects.filter(nombre='Sucursal Norte').exists())

	def test_ti_can_register_department(self):
		self.client.force_login(self.ti_user)

		response = self.client.post(reverse('catalogos:departments'), {
			'nombre': 'Operaciones',
			'descripcion': 'Área operativa',
			'activo': 'on',
		})

		self.assertRedirects(response, reverse('catalogos:departments'))
		self.assertTrue(Departamento.objects.filter(nombre='Operaciones').exists())

	def test_rh_can_edit_catalog_record(self):
		branch = Sucursal.objects.create(nombre='Sucursal Centro', ciudad='Saltillo')
		self.client.force_login(self.rh_user)

		response = self.client.post(reverse('catalogos:edit-branch', args=[branch.pk]), {
			'nombre': 'Sucursal Centro Actualizada',
			'ciudad': 'Saltillo',
			'direccion': '',
			'activa': 'on',
		})

		self.assertRedirects(response, reverse('catalogos:branches'))
		self.assertTrue(Sucursal.objects.filter(nombre='Sucursal Centro Actualizada').exists())

	def test_ti_can_toggle_and_delete_catalog_record(self):
		position = Puesto.objects.create(nombre='Auxiliar')
		self.client.force_login(self.ti_user)

		response = self.client.post(reverse('catalogos:toggle-position', args=[position.pk]))

		self.assertRedirects(response, reverse('catalogos:positions'))
		position.refresh_from_db()
		self.assertFalse(position.activo)

		response = self.client.post(reverse('catalogos:delete-position', args=[position.pk]))

		self.assertRedirects(response, reverse('catalogos:positions'))
		self.assertFalse(Puesto.objects.filter(pk=position.pk).exists())

	def test_duplicate_name_shows_friendly_error(self):
		Sucursal.objects.create(nombre='Sucursal Centro', ciudad='Saltillo')
		self.client.force_login(self.rh_user)

		response = self.client.post(reverse('catalogos:branches'), {
			'nombre': 'Sucursal Centro',
			'ciudad': 'Monterrey',
			'direccion': '',
			'activa': 'on',
		})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Ese nombre ya está registrado')
		self.assertContains(response, 'catalog-message-catalog-duplicate')
