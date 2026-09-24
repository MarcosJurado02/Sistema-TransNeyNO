from django.test import TestCase

from .models import Empleado


class CoreSmokeTests(TestCase):
	def test_core_tests_are_discoverable(self):
		self.assertTrue(True)

	def test_employees_allow_repeated_numbers_and_missing_optional_data(self):
		first = Empleado.objects.create(nombre='Empleado uno', numero_empleado='1475')
		second = Empleado.objects.create(nombre='Empleado dos', numero_empleado='1475')

		self.assertNotEqual(first.pk, second.pk)
		self.assertEqual(first.numero_empleado, second.numero_empleado)
		self.assertIsNone(first.sucursal)
		self.assertIsNone(first.tipo_empleado)
		self.assertIsNone(first.fecha_alta)
		self.assertIsNone(first.fecha_baja)
