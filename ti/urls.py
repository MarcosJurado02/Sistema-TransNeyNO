from django.urls import path

from . import views

app_name = 'ti'

urlpatterns = [
    path('inventario/', views.inventory, name='inventory'),
    path('impresoras/', views.printers, name='printers'),
    path('impresoras/registrar/', views.register_printer, name='register-printer'),
    path('impresoras/<int:pk>/editar/', views.edit_printer, name='edit-printer'),
    path('impresoras/<int:pk>/baja/', views.retire_printer, name='retire-printer'),
]