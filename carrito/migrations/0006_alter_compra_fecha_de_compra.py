# Generated by Django 5.0.2 on 2024-07-09 21:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrito', '0005_compra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='fecha_de_compra',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha de compra'),
        ),
    ]