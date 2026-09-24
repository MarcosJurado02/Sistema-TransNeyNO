from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse


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
