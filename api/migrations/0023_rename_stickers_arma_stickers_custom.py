# Generated by Django 5.0.2 on 2024-07-10 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_arma_localized_tag_name_arma_stickers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arma',
            old_name='stickers',
            new_name='stickers_custom',
        ),
    ]