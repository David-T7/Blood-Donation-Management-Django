# Generated by Django 2.2.7 on 2022-03-31 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Event', '0002_auto_20220330_2024'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Event',
            new_name='Events',
        ),
    ]