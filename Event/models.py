from contextlib import nullcontext
from django.db import models
import uuid
from django_google_maps import fields as map_fields
from location_field.models.plain import PlainLocationField

class Event(models.Model):
    Event_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    EventName = models.CharField(max_length=10)
    EventDate = models.DateField(max_length=20)
    EventPlace = models.CharField(max_length=50)
    EventTime = models.TimeField()
    EventType = models.CharField(max_length=10)
    EventPic= models.FileField(null=True, blank=True, upload_to='events/', default="events/defaultevent.png")


class Camp(models.Model):
    Camps_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    CampsName = models.CharField(max_length=10)
    CampsWoreda = models.CharField(max_length=50)
    CampsKebele = models.IntegerField()
    city = models.CharField(max_length=255 , null=True)
    location = PlainLocationField(based_fields=['city'], zoom=7 , null =True)
