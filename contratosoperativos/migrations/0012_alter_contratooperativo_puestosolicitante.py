# Generated by Django 4.2.3 on 2023-08-23 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratosoperativos', '0011_alter_contratooperativo_puestotestigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratooperativo',
            name='puestoSolicitante',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
