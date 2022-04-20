from django.db import models
import uuid

from pyrsistent import field
from Blood.models import Blood
from UserAccount.models import Address , Account

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

class Hospital(models.Model):
    Hospital_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Username = models.CharField(max_length=20, null=True , blank=True)
    HospitalName = models.CharField(max_length=20, null=True , blank=True)
    Address_id = models.OneToOneField(Address, on_delete=models.CASCADE , null=True , blank=True)
    BranchNo= models.CharField(max_length=10)
    HospitalRepresentative = models.CharField(max_length=10)
    ProfilePic= models.FileField(null=True, blank=True, upload_to='profilepic/', default="profilepic/defaultprofile.jpeg.")
    def __str__(self):
        return str(self.Hospital_id)
    

class BloodRequest(models.Model):
    Blood_Req_Id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Hospital_id = models.ForeignKey(Hospital , null=True , on_delete= models.SET_NULL,blank=True , unique=False)
    Blood_id =   models.ForeignKey(Blood , null=True , on_delete=models.SET_NULL,blank=True , unique=False)
    Blood_Group = models.CharField(max_length=10 , choices=blood_type,  null=True , blank=True)
    Quantity = models.CharField(max_length=10 , null=True , blank=True)
    Request_Date = models.DateTimeField(auto_now_add=True , null=True , blank=True)
    Status = models.CharField(max_length=12 , null=True , blank= True , default='in progress')

class HospitalSentBloods(models.Model):
     Blood_Req_Id = models.UUIDField(null=True , blank=True )
     Blood_id = models.UUIDField(null=True , blank=True )