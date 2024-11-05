# Generated by Django 4.2.2 on 2023-07-12 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='impMensualBruto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='noContrato',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]