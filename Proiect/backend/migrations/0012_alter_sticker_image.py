# Generated by Django 4.2.7 on 2023-11-14 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_alter_sticker_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]