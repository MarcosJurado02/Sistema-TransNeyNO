from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Impresora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sucursal', models.CharField(blank=True, max_length=100)),
                ('ubicacion', models.CharField(blank=True, max_length=150)),
                ('marca', models.CharField(blank=True, max_length=80)),
                ('modelo', models.CharField(blank=True, max_length=120)),
                ('numero_serie', models.CharField(blank=True, max_length=120)),
                ('mac', models.CharField(blank=True, max_length=60)),
                ('ip', models.CharField(blank=True, max_length=50)),
                ('usuario', models.CharField(blank=True, max_length=100)),
                ('contrasena', models.CharField(blank=True, max_length=150)),
                ('estatus', models.CharField(blank=True, max_length=100)),
                ('toner', models.CharField(blank=True, max_length=150)),
                ('proveedor', models.CharField(blank=True, max_length=150)),
                ('nombre_proveedor', models.CharField(blank=True, max_length=150)),
                ('numero_a_reportar', models.CharField(blank=True, max_length=100)),
                ('activa', models.BooleanField(default=True)),
                ('fecha_baja', models.DateField(blank=True, null=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Impresora', 'verbose_name_plural': 'Impresoras', 'ordering': ['sucursal', 'ubicacion', 'marca']},
        ),
    ]