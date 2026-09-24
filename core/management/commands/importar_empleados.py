import re
import unicodedata
from datetime import date, datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import Empleado, JefeDirecto, Sucursal, TipoEmpleado

try:
    from openpyxl import load_workbook
except ImportError:  # pragma: no cover - reported as a command error
    load_workbook = None


PLACEHOLDERS = {
    '',
    'jefe directo',
    'puesto',
    'puestos',
    'sucursal',
    'sucursales',
    'selecciona',
    'selecciona una sucursal',
    'sin especificar',
    'n/a',
    'na',
    'no aplica',
}


class Command(BaseCommand):
    help = 'Importa empleados desde un archivo XLSX y enlaza sus jefes por nombre.'

    def add_arguments(self, parser):
        parser.add_argument('archivo', nargs='?', default='base de empleados.xlsx')
        parser.add_argument('--dry-run', action='store_true', help='Revisar sin guardar cambios.')
        parser.add_argument('--append', action='store_true', help='Permitir importar aunque ya existan empleados.')

    def handle(self, *args, **options):
        if load_workbook is None:
            raise CommandError('Falta openpyxl. Instálalo con: pip install openpyxl')

        path = Path(options['archivo'])
        if not path.exists():
            raise CommandError(f'No existe el archivo: {path}')

        if Empleado.objects.exists() and not options['append']:
            raise CommandError(
                'Ya existen empleados. Usa --append para agregar registros sin borrar los actuales.'
            )

        rows = self._read_rows(path)
        branches = self._catalog_map(Sucursal.objects.all())
        employee_types = self._catalog_map(TipoEmpleado.objects.all())
        direct_bosses = self._catalog_map(JefeDirecto.objects.filter(activo=True))
        prepared, report = self._prepare_rows(rows, branches, employee_types, direct_bosses)

        self._print_report(report, len(prepared))
        if options['dry_run']:
            self.stdout.write(self.style.WARNING('Modo revisión: no se guardaron cambios.'))
            return

        with transaction.atomic():
            created = [Empleado.objects.create(**item['fields']) for item in prepared]
            linked = 0
            for item, employee in zip(prepared, created):
                if item['boss'] is not None:
                    employee.jefe_directo = item['boss']
                    employee.save(update_fields=('jefe_directo',))
                    linked += 1

        self.stdout.write(self.style.SUCCESS(f'Importación completada: {len(created)} empleados.'))
        self.stdout.write(f'Jefes relacionados: {linked}')

    def _read_rows(self, path):
        workbook = load_workbook(path, read_only=True, data_only=True)
        worksheet = workbook.active
        rows = []
        for row_number, values in enumerate(worksheet.iter_rows(min_row=2, values_only=True), start=2):
            values = list(values) + [None] * (11 - len(values))
            if not self._clean(values[1]):
                continue
            rows.append((row_number, values[:11]))
        return rows

    def _prepare_rows(self, rows, branches, employee_types, direct_bosses):
        prepared = []
        report = {
            'skipped_without_name': 0,
            'missing_branch': 0,
            'unknown_branch': 0,
            'missing_type': 0,
            'unknown_type': 0,
            'missing_position': 0,
            'missing_dates': 0,
            'invalid_dates': 0,
            'inactive': 0,
            'boss_missing': 0,
        }

        for row_number, values in rows:
            number, name, employee_type, branch, position, hire_date, leave_date, boss, _boss_position, _boss_branch, marker = values
            name = self._clean(name)
            branch = self._clean(branch)
            employee_type = self._clean(employee_type)
            position = self._clean(position)
            boss = self._clean(boss)
            hire_date = self._parse_date(hire_date)
            leave_date = self._parse_date(leave_date)
            inactive = self._clean(marker).casefold() == 'baja' or leave_date is not None

            branch_object = branches.get(self._key(branch)) if branch else None
            type_object = employee_types.get(self._key(employee_type)) if employee_type else None
            boss_object = direct_bosses.get(self._key(boss)) if boss else None
            if not branch:
                report['missing_branch'] += 1
            elif branch_object is None:
                report['unknown_branch'] += 1
            if not employee_type:
                report['missing_type'] += 1
            elif type_object is None:
                report['unknown_type'] += 1
            if not position:
                report['missing_position'] += 1
            if hire_date is None:
                report['missing_dates'] += 1
            if leave_date is not None and inactive:
                report['inactive'] += 1
            if boss and boss not in PLACEHOLDERS and boss_object is None:
                report['boss_missing'] += 1

            prepared.append({
                'fields': {
                    'numero_empleado': self._clean_number(number),
                    'nombre': name,
                    'tipo_empleado': type_object,
                    'puesto': position or '',
                    'sucursal': branch_object,
                    'activo': not inactive,
                    'fecha_alta': hire_date,
                    'fecha_baja': leave_date,
                },
                'name_key': self._key(name),
                'boss_key': self._key(boss) if boss and boss not in PLACEHOLDERS else '',
                'boss': boss_object,
                'row_number': row_number,
            })

        duplicate_numbers = self._duplicate_numbers(prepared)
        report['duplicate_numbers'] = duplicate_numbers
        report['unresolved_bosses'] = report['boss_missing']
        return prepared, report

    def _print_report(self, report, total):
        self.stdout.write(f'Registros a importar: {total}')
        self.stdout.write(f'Con baja: {report["inactive"]}')
        self.stdout.write(f'Sin sucursal: {report["missing_branch"]}')
        self.stdout.write(f'Sucursal no encontrada: {report["unknown_branch"]}')
        self.stdout.write(f'Sin tipo de empleado: {report["missing_type"]}')
        self.stdout.write(f'Tipo no encontrado: {report["unknown_type"]}')
        self.stdout.write(f'Sin puesto: {report["missing_position"]}')
        self.stdout.write(f'Sin fecha de alta: {report["missing_dates"]}')
        self.stdout.write(f'Jefes sin coincidencia única: {report["unresolved_bosses"]}')
        self.stdout.write(f'Números repetidos permitidos: {report["duplicate_numbers"]}')

    @staticmethod
    def _catalog_map(items):
        return {Command._key(item.nombre): item for item in items}

    @staticmethod
    def _clean(value):
        if value is None:
            return ''
        value = str(value).strip()
        return '' if value.casefold() in PLACEHOLDERS else value

    @staticmethod
    def _clean_number(value):
        if value is None or value == '':
            return None
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value).strip()

    @staticmethod
    def _key(value):
        value = unicodedata.normalize('NFKD', value or '')
        value = ''.join(char for char in value if not unicodedata.combining(char))
        return re.sub(r'\s+', ' ', value).strip().casefold()

    @staticmethod
    def _parse_date(value):
        if value in (None, ''):
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        text = str(value).strip()
        for pattern in ('%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'):
            try:
                return datetime.strptime(text, pattern).date()
            except ValueError:
                continue
        return None

    @staticmethod
    def _duplicate_numbers(items):
        counts = {}
        for item in items:
            number = item['fields']['numero_empleado']
            if number:
                counts[number] = counts.get(number, 0) + 1
        return sum(count - 1 for count in counts.values() if count > 1)
