# Generated by Django 5.0.2 on 2024-05-04 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_arma_full_item_name_alter_arma_high_rank_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arma',
            name='a',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='d',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='full_item_name',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='imageurl',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='item_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='m',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='origin_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='quality_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='rarity_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='s',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='weapon_type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='arma',
            name='wear_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]