# Generated by Django 4.2.3 on 2023-08-08 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_remove_order_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]