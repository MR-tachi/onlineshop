# Generated by Django 4.0 on 2022-08-09 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(max_length=250),
        ),
    ]
