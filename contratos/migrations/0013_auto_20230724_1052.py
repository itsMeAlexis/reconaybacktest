# Generated by Django 3.2.7 on 2023-07-24 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0012_auto_20230718_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='pdf1',
            field=models.ImageField(blank=True, null=True, upload_to='contratosPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf2',
            field=models.ImageField(blank=True, null=True, upload_to='contratosPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf3',
            field=models.ImageField(blank=True, null=True, upload_to='contratosPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf4',
            field=models.ImageField(blank=True, null=True, upload_to='contratosPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf5',
            field=models.ImageField(blank=True, null=True, upload_to='contratosPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf6',
            field=models.ImageField(blank=True, null=True, upload_to='contratosPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf7',
            field=models.ImageField(blank=True, null=True, upload_to='contratosPDF'),
        ),
        migrations.AlterField(
            model_name='contrato',
            name='pdf8',
            field=models.ImageField(blank=True, null=True, upload_to='contratosPDF'),
        ),
    ]