# Generated by Django 4.2.3 on 2023-11-19 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratosoperativos', '0013_contratooperativo_cppds'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratooperativo',
            name='domicilioSecretaria',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='contratooperativo',
            name='nombreVobo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contratooperativo',
            name='puestoVobo',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='contratooperativo',
            name='sueldoAnterior',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='contratooperativo',
            name='tipoContrato',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='contratooperativo',
            name='cpPdS',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
