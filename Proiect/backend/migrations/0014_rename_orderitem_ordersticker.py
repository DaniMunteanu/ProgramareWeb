# Generated by Django 4.2.7 on 2023-11-14 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_remove_order_customer_order_user_delete_customer'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderItem',
            new_name='OrderSticker',
        ),
    ]