from django.urls import path

from . import views

app_name = 'rh'

urlpatterns = [
    path('empleados/', views.employees, name='employees'),
    path('empleados/registrados/', views.employee_list, name='employee-list'),
    path('empleados/registrar/', views.employee_create, name='employee-create'),
    path('empleados/<int:pk>/editar/', views.employee_edit, name='employee-edit'),
    path('empleados/<int:pk>/baja/', views.employee_retire, name='employee-retire'),
]