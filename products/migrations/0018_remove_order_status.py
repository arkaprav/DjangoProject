# Generated by Django 4.2.3 on 2023-08-08 05:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='Status',
        ),
    ]