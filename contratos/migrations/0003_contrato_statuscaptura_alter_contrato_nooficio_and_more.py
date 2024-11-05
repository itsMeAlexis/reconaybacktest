# Generated by Django 4.2.2 on 2023-07-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0002_alter_contrato_impmensualbruto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='statusCaptura',
            field=models.BooleanField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='NoOficio',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='cedulaProf',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='curpdS',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='domicilioPdS',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='edadPdS',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='emailPdS',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='estadoCivilPdS',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='funcionesProf',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='inePdS',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='institucionExpTituloProf',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='nombrePdS',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='nombreSecretaria',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='nombreSecretario',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='nombreSolicitante',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='nombreTestigo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='operativoProf',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='puestoSecretario',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='puestoSolicitante',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='puestoTestigo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='rfcPdS',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='sexoPdS',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='statusFirma',
            field=models.BooleanField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='tituloProf',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
