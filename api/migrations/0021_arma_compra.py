# Generated by Django 5.0.2 on 2024-07-09 21:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_arma_habilitada'),
        ('carrito', '0006_alter_compra_fecha_de_compra'),
    ]

    operations = [
        migrations.AddField(
            model_name='arma',
            name='compra',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='armas_compradas', to='carrito.compra'),
        ),
    ]