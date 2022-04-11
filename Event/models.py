from django.db import models
import uuid
class Event(models.Model):
    Event_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    EventName = models.CharField(max_length=10)
    EventDate = models.DateField(max_length=20)
    EventPlace = models.CharField(max_length=50)
    EventTime = models.TimeField()
    EventType = models.CharField(max_length=10)

class Camp(models.Model):
    Camps_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    CampsName = models.CharField(max_length=10)
    CampsWoreda = models.CharField(max_length=50)
    CampsKebele = models.IntegerField()
    CampsPlace = models.CharField(max_length=10) 