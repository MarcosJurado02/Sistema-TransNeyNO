from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from core.models import Empleado, Sucursal


class HumanResourcesAccessTests(TestCase):
	def setUp(self):
		self.rh_user = User.objects.create_user(username='rh-user', password='test-pass')
		self.rh_user.groups.add(Group.objects.create(name='RH'))
		self.general_user = User.objects.create_user(username='general-user', password='test-pass')
		self.admin = User.objects.create_user(
			username='admin-user',
			password='test-pass',
			is_staff=True,
		)
		sucursal = Sucursal.objects.create(nombre='Oficina central', ciudad='Monterrey')
		Empleado.objects.create(
			numero_empleado='RH-001',
			nombre='Ana Torres',
			puesto='Analista de RH',
			area='Recursos humanos',
			sucursal=sucursal,
		)

	def test_rh_user_can_see_registered_employees(self):
		self.client.force_login(self.rh_user)

		response = self.client.get(reverse('rh:employee-list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Ana Torres')
		self.assertContains(response, 'Todos los empleados registrados')
		self.assertContains(response, 'Histórico')
		self.assertContains(response, 'Empleados')
		self.assertContains(response, 'Alta de empleado')

	def test_admin_can_see_registered_employees(self):
		self.client.force_login(self.admin)

		response = self.client.get(reverse('rh:employee-list'))

		self.assertEqual(response.status_code, 200)

	def test_user_without_rh_access_is_forbidden(self):
		self.client.force_login(self.general_user)

		response = self.client.get(reverse('rh:employees'))

		self.assertEqual(response.status_code, 403)

	def test_rh_submenu_only_appears_inside_rh(self):
		self.client.force_login(self.rh_user)

		dashboard_response = self.client.get(reverse('core:dashboard'))
		rh_response = self.client.get(reverse('rh:employees'))

		self.assertContains(dashboard_response, 'Histórico')
		self.assertContains(dashboard_response, 'Empleados')
		self.assertContains(dashboard_response, 'Alta de empleado')
		self.assertNotContains(rh_response, 'Ana Torres')
		self.assertContains(rh_response, 'Histórico')
		self.assertContains(rh_response, 'Empleados')
		self.assertContains(rh_response, 'Alta de empleado')

	def test_employee_table_only_appears_in_employee_submodule(self):
		self.client.force_login(self.rh_user)

		module_response = self.client.get(reverse('rh:employees'))
		list_response = self.client.get(reverse('rh:employee-list'))

		self.assertNotContains(module_response, 'Ana Torres')
		self.assertContains(list_response, 'Ana Torres')
