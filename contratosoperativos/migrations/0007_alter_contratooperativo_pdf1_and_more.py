# Generated by Django 4.2.3 on 2023-08-07 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratosoperativos', '0006_alter_contratooperativo_funcionespsd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratooperativo',
            name='pdf1',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contratooperativo',
            name='pdf2',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contratooperativo',
            name='pdf3',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contratooperativo',
            name='pdf4',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contratooperativo',
            name='pdf5',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contratooperativo',
            name='pdf6',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contratooperativo',
            name='pdf7',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
        migrations.AlterField(
            model_name='contratooperativo',
            name='pdf8',
            field=models.FileField(blank=True, null=True, upload_to='documentacionPDF'),
        ),
    ]