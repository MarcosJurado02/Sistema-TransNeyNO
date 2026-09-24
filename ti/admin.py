from django.contrib import admin

from .models import Impresora


@admin.register(Impresora)
class ImpresoraAdmin(admin.ModelAdmin):
	list_display = ('sucursal', 'ubicacion', 'marca', 'modelo', 'ip', 'activa')
	list_filter = ('activa', 'marca', 'sucursal')
	search_fields = ('sucursal', 'ubicacion', 'marca', 'modelo', 'numero_serie', 'ip')
