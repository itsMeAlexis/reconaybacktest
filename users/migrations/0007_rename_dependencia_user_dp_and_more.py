# Generated by Django 4.2.3 on 2023-08-21 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_clave'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='dependencia',
            new_name='DP',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='dependencia_id',
            new_name='nombreDependencia',
        ),
    ]