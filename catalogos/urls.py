from django.urls import path

from . import views

app_name = 'catalogos'

urlpatterns = [
	path('', views.catalogs, name='home'),
	path('sucursales/', views.sucursales, name='branches'),
	path('sucursales/<int:pk>/editar/', views.editar_sucursal, name='edit-branch'),
	path('sucursales/<int:pk>/eliminar/', views.eliminar_sucursal, name='delete-branch'),
	path('sucursales/<int:pk>/estado/', views.cambiar_estado_sucursal, name='toggle-branch'),
	path('departamentos/', views.departamentos, name='departments'),
	path('departamentos/<int:pk>/editar/', views.editar_departamento, name='edit-department'),
	path('departamentos/<int:pk>/eliminar/', views.eliminar_departamento, name='delete-department'),
	path('departamentos/<int:pk>/estado/', views.cambiar_estado_departamento, name='toggle-department'),
	path('puestos/', views.puestos, name='positions'),
	path('puestos/<int:pk>/editar/', views.editar_puesto, name='edit-position'),
	path('puestos/<int:pk>/eliminar/', views.eliminar_puesto, name='delete-position'),
	path('puestos/<int:pk>/estado/', views.cambiar_estado_puesto, name='toggle-position'),
	path('tipos-empleado/', views.tipos_empleado, name='employee-types'),
	path('tipos-empleado/<int:pk>/editar/', views.editar_tipo_empleado, name='edit-employee-type'),
	path('tipos-empleado/<int:pk>/eliminar/', views.eliminar_tipo_empleado, name='delete-employee-type'),
	path('tipos-empleado/<int:pk>/estado/', views.cambiar_estado_tipo_empleado, name='toggle-employee-type'),
	path('jefes-directos/', views.jefes_directos, name='direct-bosses'),
	path('jefes-directos/<int:pk>/editar/', views.editar_jefe_directo, name='edit-direct-boss'),
	path('jefes-directos/<int:pk>/eliminar/', views.eliminar_jefe_directo, name='delete-direct-boss'),
	path('jefes-directos/<int:pk>/estado/', views.cambiar_estado_jefe_directo, name='toggle-direct-boss'),
]