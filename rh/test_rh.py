from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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
		self.employee_branch = Sucursal.objects.create(nombre='Oficina central', ciudad='Monterrey')
		Empleado.objects.create(
			numero_empleado='RH-001',
			nombre='Ana Torres',
			puesto='Analista de RH',
			area='Recursos humanos',
			sucursal=self.employee_branch,
		)

	def test_rh_user_can_see_registered_employees(self):
		self.client.force_login(self.rh_user)

		response = self.client.get(reverse('rh:employee-list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Ana Torres')
		self.assertContains(response, 'Todos los empleados registrados')
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

		self.assertContains(dashboard_response, 'Empleados')
		self.assertContains(dashboard_response, 'Alta de empleado')
		self.assertNotContains(rh_response, 'Histórico')
		self.assertContains(rh_response, 'Empleados')
		self.assertContains(rh_response, 'Alta de empleado')

	def test_employee_table_only_appears_in_employee_submodule(self):
		self.client.force_login(self.rh_user)

		module_response = self.client.get(reverse('rh:employees'))
		list_response = self.client.get(reverse('rh:employee-list'))

		self.assertNotContains(module_response, 'Ana Torres')
		self.assertContains(list_response, 'Ana Torres')

	def test_active_tab_hides_leave_date_and_form_hides_status_fields(self):
		self.client.force_login(self.rh_user)

		list_response = self.client.get(reverse('rh:employee-list'))
		form_response = self.client.get(reverse('rh:employee-create'))

		self.assertNotContains(list_response, 'Fecha de baja')
		self.assertNotContains(form_response, 'Fecha de baja')
		self.assertNotContains(form_response, 'Activo')

	def test_retiring_employee_moves_to_inactive_tab_with_today_date(self):
		self.client.force_login(self.rh_user)
		empleado = Empleado.objects.get(nombre='Ana Torres')

		response = self.client.post(reverse('rh:employee-retire', args=(empleado.pk,)))

		empleado.refresh_from_db()
		self.assertRedirects(response, reverse('rh:employee-list'))
		self.assertFalse(empleado.activo)
		self.assertEqual(empleado.fecha_baja, timezone.localdate())
		self.assertContains(self.client.get(f'{reverse("rh:employee-list")}?tab=inactive'), 'Ana Torres')

	def test_employee_list_can_filter_by_branch(self):
		self.client.force_login(self.rh_user)

		response = self.client.get(reverse('rh:employee-list'), {'sucursal': self.employee_branch.pk})

		self.assertContains(response, 'Ana Torres')
		self.assertEqual(response.context['total_empleados'], 1)

	def test_employee_list_can_search_by_name(self):
		self.client.force_login(self.rh_user)

		response = self.client.get(reverse('rh:employee-list'), {'nombre': 'Ana'})

		self.assertContains(response, 'Ana Torres')
		self.assertEqual(response.context['total_empleados'], 1)
