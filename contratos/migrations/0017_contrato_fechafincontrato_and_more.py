# Generated by Django 4.2.3 on 2023-08-02 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0016_auto_20230724_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='fechaFinContrato',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='contrato',
            name='fechaInicioContrato',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
