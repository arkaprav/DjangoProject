# Generated by Django 4.2.3 on 2023-08-05 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_items_item_id_alter_items_item_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_id',
            new_name='user_id',
        ),
        migrations.AddField(
            model_name='order',
            name='Address',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='PaymentStatus',
            field=models.CharField(default=None, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='order_items',
            field=models.ManyToManyField(blank=True, to='products.items'),
        ),
    ]
