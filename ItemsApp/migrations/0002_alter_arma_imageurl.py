# Generated by Django 5.0.2 on 2024-02-22 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ItemsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arma',
            name='imageurl',
            field=models.URLField(),
        ),
    ]