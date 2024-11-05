# Generated by Django 4.2.2 on 2023-07-09 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dependencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreDependencia', models.CharField(max_length=200)),
                ('RM', models.CharField(max_length=10)),
                ('DP', models.CharField(max_length=10)),
                ('SD', models.CharField(max_length=10)),
                ('DG', models.CharField(max_length=10)),
                ('DA', models.CharField(max_length=10)),
                ('UR', models.CharField(max_length=10)),
                ('NoUR', models.CharField(max_length=10)),
                ('image', models.ImageField(upload_to='dependencias')),
            ],
        ),
    ]
