# Generated by Django 5.0.2 on 2024-07-05 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_arma_inspect_link'),
        ('carrito', '0004_remove_carrito_contenido_carrito_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arma',
            name='carrito',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='armas', to='carrito.carrito'),
        ),
    ]