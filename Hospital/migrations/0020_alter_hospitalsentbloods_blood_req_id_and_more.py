# Generated by Django 4.0.3 on 2022-04-20 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hospital', '0019_alter_hospitalsentbloods_blood_req_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalsentbloods',
            name='Blood_Req_Id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hospitalsentbloods',
            name='Blood_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
