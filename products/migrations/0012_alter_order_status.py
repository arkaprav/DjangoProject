# Generated by Django 4.2.3 on 2023-08-08 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='Status',
            field=models.CharField(choices=[(1, 'In Progress'), (0, 'Cancelled'), (10, 'Completed')], default=1, max_length=20),
        ),
    ]