from django.db import models


class Sucursal(models.Model):
	nombre = models.CharField(max_length=100, unique=True)
	ciudad = models.CharField(max_length=100)
	direccion = models.CharField(max_length=255, blank=True)
	activa = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Sucursal'
		verbose_name_plural = 'Sucursales'
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


class Departamento(models.Model):
	nombre = models.CharField(max_length=100, unique=True)
	descripcion = models.CharField(max_length=255, blank=True)
	activo = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Departamento'
		verbose_name_plural = 'Departamentos'
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


class Puesto(models.Model):
	nombre = models.CharField(max_length=100, unique=True)
	descripcion = models.CharField(max_length=255, blank=True)
	activo = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Puesto'
		verbose_name_plural = 'Puestos'
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


class TipoEmpleado(models.Model):
	nombre = models.CharField(max_length=100, unique=True)
	descripcion = models.CharField(max_length=255, blank=True)
	activo = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Tipo de empleado'
		verbose_name_plural = 'Tipos de empleado'
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


class JefeDirecto(models.Model):
	nombre = models.CharField(max_length=150, unique=True)
	activo = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Jefe directo'
		verbose_name_plural = 'Jefes directos'
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


class Empleado(models.Model):
	numero_empleado = models.CharField(max_length=20, null=True, blank=True)
	nombre = models.CharField(max_length=150)
	tipo_empleado = models.ForeignKey(
		TipoEmpleado,
		on_delete=models.PROTECT,
		null=True,
		blank=True,
		related_name='empleados',
	)
	puesto = models.CharField(max_length=100, blank=True)
	area = models.CharField(max_length=100, blank=True)
	sucursal = models.ForeignKey(
		Sucursal,
		on_delete=models.PROTECT,
		null=True,
		blank=True,
		related_name='empleados',
	)
	jefe_directo = models.ForeignKey(
		JefeDirecto,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='empleados',
	)
	correo_institucional = models.EmailField(blank=True)
	activo = models.BooleanField(default=True)
	fecha_alta = models.DateField(null=True, blank=True)
	fecha_baja = models.DateField(null=True, blank=True)

	class Meta:
		verbose_name = 'Empleado'
		verbose_name_plural = 'Empleados'
		ordering = ['nombre']

	def __str__(self):
		return f'{self.nombre} (baja)' if not self.activo else self.nombre
