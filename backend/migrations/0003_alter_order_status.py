# Generated by Django 5.2 on 2025-05-01 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_rename_imageurl_product_imageurl_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Pending', 'Pending'), ('Canceled', 'Canceled')], default='PENDING', max_length=20),
        ),
    ]
