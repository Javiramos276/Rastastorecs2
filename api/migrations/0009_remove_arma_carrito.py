# Generated by Django 5.0.2 on 2024-05-08 03:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_arma_carrito'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arma',
            name='carrito',
        ),
    ]