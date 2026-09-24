from .models import Empleado


def employee_profile(request):
    empleado = None
    is_admin = False
    can_view_inventory = False
    can_view_maintenance = False
    can_view_hr = False
    can_view_catalogs = False

    if request.user.is_authenticated:
        empleado = Empleado.objects.filter(
            numero_empleado=request.user.get_username(),
            activo=True,
        ).first()
        group_names = set(request.user.groups.values_list('name', flat=True))
        is_admin = request.user.is_superuser or request.user.is_staff or bool(
            group_names.intersection({'Admin', 'Administradores'})
        )
        can_view_inventory = is_admin or bool(
            group_names.intersection({'TI', 'Inventario TI'})
        )
        can_view_maintenance = is_admin or 'Mantenimiento' in group_names
        can_view_hr = is_admin or bool(
            group_names.intersection({'RH', 'Recursos Humanos'})
        )
        can_view_catalogs = is_admin or bool(
            group_names.intersection({'RH', 'Recursos Humanos', 'TI', 'Inventario TI'})
        )

    return {
        'empleado': empleado,
        'is_admin': is_admin,
        'can_view_inventory': can_view_inventory,
        'can_view_maintenance': can_view_maintenance,
        'can_view_hr': can_view_hr,
        'can_view_catalogs': can_view_catalogs,
    }