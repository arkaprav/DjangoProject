# Generated by Django 4.2.3 on 2023-08-08 05:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='Date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
