from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ti', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='impresora',
            name='motivo_baja',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]