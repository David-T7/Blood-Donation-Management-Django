from contextlib import nullcontext
from django.db import models
import uuid

class Event(models.Model):
    Event_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    EventName = models.CharField(max_length=20)
    EventDate = models.DateField(max_length=20)
    EventPlace = models.CharField(max_length=50)
    EventDescription = models.CharField(max_length=150 , null=True) 
    EventDate = models.DateField()
    EventType = models.CharField(max_length=10)
    EventPic= models.FileField(null=True, blank=True, upload_to='events/', default="events/defaultevent.png")
    class Meta:
        db_table = "Event"


class Camp(models.Model):
    Camps_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    CampsName = models.CharField(max_length=10)
    CampsWoreda = models.CharField(max_length=50)
    CampsKebele = models.IntegerField()
    city = models.CharField(max_length=255 , null=True)
    Location = models.CharField(max_length=1000 ,null=True)
    CampPic= models.FileField(null=True, blank=True, upload_to='camps/', default="camps/defaultcamp.png")
    class Meta:
        db_table = "Camp"
    
