# Generated by Django 3.2.7 on 2023-07-14 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratosoperativos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contratooperativo',
            name='user_nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]