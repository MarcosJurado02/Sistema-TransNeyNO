from django.db import migrations, models


EMPLOYEE_TYPES = [
    'Administrativo',
    'Ayudante',
    'Eléctrico',
    'Mantenimiento',
    'Mecánico',
    'Operador',
    'Operativo',
    'Soldador',
    'Ventas',
    'Limpieza',
    'Vigilancia',
    'Sin especificar',
]

BRANCHES = [
    'Altamira',
    'Guadalajara',
    'Lazaro Cardenas',
    'Manzanillo',
    'Mexico',
    'Monterrey',
    'Puebla',
    'Queretaro',
    'San Luis Potosi',
    'Veracruz',
    'Operador Foraneo',
]

POSITIONS = [
    'Gerente de Consolidado',
    'Gerente de Tesoreria y Carga General',
    'Gerente Carga General',
    'Gerente de Monitoreo',
    'Gerente de Sistemas',
    'Gerente de Contabilidad',
    'Gerente de Facturacion y Cobranza',
    'Gerente de Recursos Humanos y Nomina',
    'Mantenimiento',
    'Coordinador de Importaciones',
    'Coordinador de Exportaciones',
    'Auxiliar de Operaciones',
    'Coordinador de Trafico Contenedores',
    'Atencion a Clientes',
    'Sistema de Gestion y Mejora Continua',
    'Auxiliar de Sistema de Gestion y Mejora Continua',
    'Control Medico',
    'Autoconsumo',
    'Ejecutivo de Ventas',
    'Coordinador de Operaciones NH',
    'Almacenista',
    'Asistente de Direccion',
    'Auxiliar de Recursos Humanos',
    'Auxiliar Contable',
    'Auxiliar de Sistemas',
    'Auxiliar de Facturacion y Cobranza',
    'Monitorista',
    'Operador Local',
    'Operador Foraneo',
    'Direccion Operativa NH',
    'Direccion General',
    'Supervisor de Almacen',
    'Gerente de Ventas',
    'Ayudante General',
    'Montacarguista',
    'Limpieza',
    'Vigilante',
    'Contabilidad',
]


def load_catalog_data(apps, schema_editor):
    Sucursal = apps.get_model('core', 'Sucursal')
    Puesto = apps.get_model('core', 'Puesto')
    TipoEmpleado = apps.get_model('core', 'TipoEmpleado')

    for nombre in EMPLOYEE_TYPES:
        TipoEmpleado.objects.get_or_create(nombre=nombre)

    for nombre in BRANCHES:
        Sucursal.objects.get_or_create(nombre=nombre, defaults={'ciudad': nombre, 'direccion': ''})

    for nombre in POSITIONS:
        Puesto.objects.get_or_create(nombre=nombre)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_departamento_puesto'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoEmpleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=255)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Tipo de empleado',
                'verbose_name_plural': 'Tipos de empleado',
                'ordering': ['nombre'],
            },
        ),
        migrations.RunPython(load_catalog_data, migrations.RunPython.noop),
    ]
