from operator import mod
from django.db import models
import uuid


# Create your models here.
class AppointmentChoice(models.Model):
    Appchoice_id =  models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Date = models.DateField()
    Time = models.TimeField()
    NumberofDonors = models.IntegerField(null=True , blank= True , default=0) 
