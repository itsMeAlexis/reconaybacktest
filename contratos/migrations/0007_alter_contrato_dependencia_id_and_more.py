# Generated by Django 4.2.2 on 2023-07-12 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0006_alter_contrato_pdf1_alter_contrato_pdf2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='dependencia_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='fechaCreacion',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='fechaOficio',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='user_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
