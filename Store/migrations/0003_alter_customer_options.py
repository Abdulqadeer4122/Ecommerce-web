# Generated by Django 5.0.4 on 2024-05-15 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_remove_customer_email_remove_customer_first_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': [('cancel_order', 'Can cancel Order')]},
        ),
    ]