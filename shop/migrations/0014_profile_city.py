# Generated by Django 4.0 on 2022-08-11 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_rename_address_order_informations_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
