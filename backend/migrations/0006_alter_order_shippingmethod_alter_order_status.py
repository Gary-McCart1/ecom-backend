# Generated by Django 5.2 on 2025-05-05 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shippingMethod',
            field=models.CharField(default='Standard', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='PENDING', max_length=20),
        ),
    ]
