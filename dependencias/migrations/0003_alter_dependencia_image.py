# Generated by Django 4.2.2 on 2023-07-09 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dependencias', '0002_alter_dependencia_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependencia',
            name='image',
            field=models.ImageField(blank=True, upload_to='dependencias'),
        ),
    ]
