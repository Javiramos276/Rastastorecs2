# Generated by Django 5.0.2 on 2024-07-10 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_arma_compra'),
    ]

    operations = [
        migrations.AddField(
            model_name='arma',
            name='localized_tag_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='arma',
            name='stickers',
            field=models.JSONField(blank=True, null=True),
        ),
    ]