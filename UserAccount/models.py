from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
rolechoice = [
      ( None, 'SelectRole'),
    ('BBManager', 'BBManager'),
    ('Nurse', 'Nurse'),
    ('LabTechnician', 'LabTechnician'),
    ('HospitalRepresentative', 'HospitalRepresentative'),
    ('Donor'  , 'Donor'),
    ]



class Account(AbstractUser):
    Role = models.CharField(max_length=25, null=True , choices=rolechoice ,  blank=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = "Account"

class Address(models.Model):
    Address_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Phone = models.IntegerField(null=True , blank=True , unique=True)
    Email = models.EmailField(null=True , blank=True , unique=True)
    City= models.CharField(max_length=20 , null=True , blank=True)
    Subcity = models.CharField(max_length=20 , null=True , blank=True )
    Woreda = models.CharField(max_length=20 , null=True , blank=True)
    PostOffice= models.CharField(max_length=9 , null=True , blank=True)
    def __str__(self):
        return str(self.Address_id)
    class Meta:
        db_table = "Address"


class UserRegistration(models.Model):
    User_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    FirstName = models.CharField(max_length=20 , null=True , blank=True)
    LastName = models.CharField(max_length=20 , null=True , blank=True)
    Address_id = models.OneToOneField(Address , on_delete=models.CASCADE)
    Age = models.IntegerField(null=True , blank=True)
    Account_id = models.OneToOneField(Account , on_delete=models.CASCADE)
    ProfilePic= models.FileField(null=True, blank=True, upload_to='profilepic/', default="profilepic/defaultprofile.jpeg")
    def __str__(self):
        return str(self.FirstName + ' ' +self.LastName)
    class Meta:
        db_table = "UserRegistration"



