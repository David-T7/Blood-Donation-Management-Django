# Generated by Django 4.0.3 on 2022-04-12 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Event', '0008_delete_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='EventPic',
            field=models.FileField(blank=True, default='events/defaultevent.png', null=True, upload_to='events/'),
        ),
    ]