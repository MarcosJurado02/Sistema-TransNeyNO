from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=255)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.CharField(blank=True, max_length=255)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Puesto',
                'verbose_name_plural': 'Puestos',
                'ordering': ['nombre'],
            },
        ),
    ]