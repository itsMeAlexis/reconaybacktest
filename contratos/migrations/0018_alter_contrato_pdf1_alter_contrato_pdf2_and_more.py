# Generated by Django 4.2.3 on 2023-08-07 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0017_contrato_fechafincontrato_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='pdf1',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf2',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf3',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf4',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf5',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf6',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf7',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf8',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
    ]
