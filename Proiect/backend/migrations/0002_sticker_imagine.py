# Generated by Django 4.2.6 on 2023-10-24 20:41

import backend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sticker',
            name='imagine',
            field=models.ImageField(blank=True),
        ),
    ]
