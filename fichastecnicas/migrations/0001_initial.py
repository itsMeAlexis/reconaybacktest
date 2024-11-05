# Generated by Django 4.2.3 on 2023-11-09 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dependencias', '0005_remove_dependencia_da_remove_dependencia_dg_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FichaTecnica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrePdS', models.CharField(blank=True, max_length=255, null=True)),
                ('telefonoPdS', models.CharField(blank=True, max_length=255, null=True)),
                ('servicioRequerido', models.CharField(blank=True, max_length=500, null=True)),
                ('areaRequiereServicio', models.CharField(blank=True, max_length=500, null=True)),
                ('domicilioUnidadAdmin', models.CharField(blank=True, max_length=255, null=True)),
                ('nombreTitularSolicitante', models.CharField(blank=True, max_length=255, null=True)),
                ('cargoTitularSolicitante', models.CharField(blank=True, max_length=255, null=True)),
                ('tipoContrato', models.CharField(blank=True, max_length=255, null=True)),
                ('fechaInicioContrato', models.CharField(blank=True, max_length=20, null=True)),
                ('fechaFinContrato', models.CharField(blank=True, max_length=20, null=True)),
                ('importeMensual', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('ajusteMensual', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('nombreSecretario', models.CharField(blank=True, max_length=200, null=True)),
                ('puestoSecretario', models.CharField(blank=True, max_length=200, null=True)),
                ('nombreVoBo', models.CharField(blank=True, max_length=200, null=True)),
                ('puestoVoBo', models.CharField(blank=True, max_length=200, null=True)),
                ('dependenciaFicha', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dependencias.dependencia')),
            ],
        ),
    ]