# Generated by Django 2.2.7 on 2022-03-26 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0002_auto_20220326_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='Phone',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]