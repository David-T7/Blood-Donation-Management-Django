from contextlib import nullcontext
from django.db import models
import uuid

class Event(models.Model):
    Event_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    EventName = models.CharField(max_length=20 , blank=False)
    EventDate = models.DateField(max_length=20 , blank=False)
    EventPlace = models.CharField(max_length=50 , blank=False)
    EventDescription = models.CharField(max_length=150 , null=True , blank=True) 
    EventType = models.CharField(max_length=10 , blank=True)
    EventPic= models.FileField(null=True, blank=True, upload_to='events/', default="events/defaultevent.png")
    class Meta:
        db_table = "Event"


class Camp(models.Model):
    Camps_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    CampsName = models.CharField(max_length=50 , blank=False)
    CampsWoreda = models.CharField(max_length=50 , null=True , blank=True)
    CampsKebele = models.IntegerField( null=True , blank=True)
    city = models.CharField(max_length=255 , null=True , blank=False)
    Location = models.CharField(max_length=1000 ,null=True , blank=False)
    CampPic= models.FileField(null=True, blank=True, upload_to='camps/', default="camps/defaultcamp.png")
    class Meta:
        db_table = "Camp"
    
