# Generated by Django 4.2.3 on 2023-07-30 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('num_products', models.PositiveIntegerField(default=0)),
                ('featured_image', models.FileField(default=None, max_length=50, null=True, upload_to='category/')),
            ],
        ),
    ]
