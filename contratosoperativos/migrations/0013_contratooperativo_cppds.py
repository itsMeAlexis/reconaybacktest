# Generated by Django 4.2.3 on 2023-11-14 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratosoperativos', '0012_alter_contratooperativo_puestosolicitante'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratooperativo',
            name='cpPdS',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
