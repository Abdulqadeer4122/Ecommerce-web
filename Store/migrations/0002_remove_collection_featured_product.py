# Generated by Django 5.0.4 on 2024-05-07 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='featured_product',
        ),
    ]
