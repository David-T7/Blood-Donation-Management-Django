# Generated by Django 4.0.3 on 2022-04-20 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blood', '0010_alter_bloodhistory_blood_id_and_more'),
        ('Hospital', '0018_alter_hospitalsentbloods_blood_req_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalsentbloods',
            name='Blood_Req_Id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Hospital.bloodrequest'),
        ),
        migrations.AlterField(
            model_name='hospitalsentbloods',
            name='Blood_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Blood.blood'),
        ),
    ]
