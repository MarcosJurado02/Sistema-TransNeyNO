def employee_profile(request):
    profile = 'Colaborador'

    if request.user.is_authenticated:
        group_names = set(request.user.groups.values_list('name', flat=True))
        if request.user.is_superuser or request.user.is_staff or group_names.intersection({'Admin', 'Administradores'}):
            profile = 'Administrador'
        elif group_names.intersection({'RH', 'Recursos Humanos'}):
            profile = 'Recursos Humanos'
        elif group_names.intersection({'TI', 'Inventario TI'}):
            profile = 'Tecnología'
        elif 'Mantenimiento' in group_names:
            profile = 'Mantenimiento'

    return {'profile': profile}