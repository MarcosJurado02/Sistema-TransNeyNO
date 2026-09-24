from django.db import models


class Impresora(models.Model):
	sucursal = models.CharField(max_length=100, blank=True)
	ubicacion = models.CharField(max_length=150, blank=True)
	marca = models.CharField(max_length=80, blank=True)
	modelo = models.CharField(max_length=120, blank=True)
	numero_serie = models.CharField(max_length=120, blank=True)
	mac = models.CharField(max_length=60, blank=True)
	ip = models.CharField(max_length=50, blank=True)
	usuario = models.CharField(max_length=100, blank=True)
	contrasena = models.CharField(max_length=150, blank=True)
	estatus = models.CharField(max_length=100, blank=True)
	toner = models.CharField(max_length=150, blank=True)
	proveedor = models.CharField(max_length=150, blank=True)
	nombre_proveedor = models.CharField(max_length=150, blank=True)
	numero_a_reportar = models.CharField(max_length=100, blank=True)
	activa = models.BooleanField(default=True)
	fecha_baja = models.DateField(null=True, blank=True)
	motivo_baja = models.CharField(max_length=255, blank=True)
	fecha_registro = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Impresora'
		verbose_name_plural = 'Impresoras'
		ordering = ['sucursal', 'ubicacion', 'marca']

	def __str__(self):
		return f'{self.marca} {self.modelo}'.strip() or f'Impresora {self.pk}'