# Generated by Django 4.0 on 2022-08-11 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='mobilephone',
            field=models.IntegerField(null=True),
        ),
    ]