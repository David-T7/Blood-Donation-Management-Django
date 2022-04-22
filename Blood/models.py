from django.db import models
import uuid
from Donor.models import Donor


blood_type = [
    ( None, 'Select type'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('A+' , 'A+'),
    ('A-' , 'A-'),
    ('B+','B+'),
     ('B-','B-'),
    ('AB+' ,'AB+'),
    ('AB-' ,'AB-'),
    ]

class Blood(models.Model):
    Blood_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Donor_id = models.ForeignKey(Donor , on_delete=models.SET_NULL, null=True , blank=True , unique=False)
    BloodGroup = models.CharField(max_length=20 ,  choices=blood_type)
    PackNo = models.CharField(max_length=20)
    RegDate = models.DateField(auto_now_add=True)
    ExpDate = models.DateField(max_length=10)
    QuantityOfBlood = models.CharField(max_length=4)


class BloodHistory(models.Model):
    Blood_id = models.UUIDField(blank=True , null=True)
    Donor_id = models.UUIDField(null=True , blank=True )
    BloodGroup = models.CharField(max_length=20 ,  choices=blood_type)
    PackNo = models.CharField(max_length=20)
    RegDate = models.DateField(max_length=10)
    ExpDate = models.DateField(max_length=10)
    QuantityOfBlood = models.CharField(max_length=4)
    Action = models.CharField(max_length=20 , null=True , blank=True)




    



  
