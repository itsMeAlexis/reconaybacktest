# Generated by Django 4.2.3 on 2023-08-06 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratosoperativos', '0005_contratooperativo_fechafincontrato_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratooperativo',
            name='funcionesPsD',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
