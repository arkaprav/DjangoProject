# Generated by Django 4.2.3 on 2023-08-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_items_item_quantity_alter_items_item_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='item_id',
            field=models.IntegerField(default=1),
        ),
    ]
