# Generated by Django 3.2.7 on 2023-07-24 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0013_auto_20230724_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrato',
            name='pdf1',
        ),
        migrations.AddField(
            model_name='contrato',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='contratosPDF'),
        ),
    ]
