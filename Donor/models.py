from cProfile import label
from datetime import datetime
from multiprocessing.sharedctypes import Value
from django.db import models
from UserAccount.models import Account, Address
import uuid
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _  # use if you support internationalization

def validate_interval(value):
    if value < 0.0:
        raise ValidationError(_('must be greater or equal to zero'), params={'value': value},)



blood_group = [
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
gender_choice = [
    ( None, 'Select Gender'),
    ('Male', 'Male'),
    ('Female', 'Female'),
]


class Donor(models.Model):
    Donor_id =  models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Account_id = models.OneToOneField(Account , on_delete=models.CASCADE ,null=True , blank=True)
    Donorname = models.CharField(max_length=20 , null=True , blank=False)
    DateOfBirth = models.DateTimeField(max_length=6, null=True , blank=False)
    Bloodgroup= models.CharField(max_length=10, null=True , blank=False , choices=blood_group)
    Address_id = models.OneToOneField(Address, on_delete=models.CASCADE , null=True , blank=True)
    Gender = models.CharField(max_length=10, null=True , blank=False , choices= gender_choice)
    Nationality = models.CharField(max_length=10, null=True , blank=True)
    Height = models.CharField(max_length=10, null=True , blank=True)
    Weight = models.CharField(max_length=10, null=True , blank=False)    
    BloodPressure = models.CharField(max_length=10 ,  null=True , blank=True)
    ProfilePic= models.FileField(null=True, blank=True, upload_to='profilepic/', default="profilepic/defaultprofile.jpeg")
    def __str__(self):
        return str(self.Donor_id)
    class Meta:
        db_table = "Donor"



class Appointment(models.Model):
    App_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Donor_id = models.ForeignKey(Donor , on_delete=models.SET_NULL, null=True , blank=True , unique=False)
    Date = models.DateField(default= datetime.now)
    Time = models.TimeField( default= datetime.now)
    status = models.CharField(null=True , max_length=12 , blank=True , default='in progress')
    def __str__(self):
        return str(self.App_id)
    class Meta:
        db_table = "Appointment"



class DonationRequestFormQuesitons(models.Model):
   Question_id = models.UUIDField( default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
   HeartDisease = models.TextField (null=True , blank=True , )
   Kidney_Lung_Bloodpressure_Diabetes_Epilepsy = models.TextField( null=True , blank=True )
   Liverproblems = models.TextField(null=True , blank=True )
   STD = models.TextField(null=True , blank=True )
   Tattoo_Ear_skin_pierced_lastmonth= models.TextField( null=True , blank=True)
   Slpet_Unsafely_OtherThanPartner = models.TextField( null=True , blank=True )
   SeriousSkinRepair = models.TextField(null=True , blank=True )
   Preagnant = models.TextField(null=True , blank=True )
   Abortion = models.TextField( null=True , blank=True )
   BreastFeeding = models.TextField( null=True , blank=True  )
   BloodHealthfulnessInfo = models.TextField( null=True , blank=True)
   def __str__(self):
        return str(self.Type)
   class Meta:
       db_table = "DonationRequestFormQuesitons"
    




Answer_choices = [
    ( None, 'Answer'),
    ('yes', 'yes'),
    ('no', 'no'),
    ]
class DonationRequestFormResult(models.Model):
    Result_id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    Donor_id = models.ForeignKey(Donor , null=True , on_delete=models.SET_NULL,blank=True , unique=False)
    HeartDisease = models.CharField(max_length=3, null=True , blank=True ,choices=Answer_choices)
    Kidney_Lung_Bloodpressure_Diabetes_Epilepsy = models.CharField(max_length=3, null=True , blank=True ,  choices=Answer_choices)
    Liverproblems = models.CharField(max_length=3, null=True , blank=True ,choices=Answer_choices)
    STD = models.CharField(max_length=3, null=True , blank=True ,choices=Answer_choices)
    Tattoo_Ear_skin_pierced_lastmonth= models.CharField(max_length=3, null=True , blank=True ,choices=Answer_choices)
    Slpet_Unsafely_OtherThanPartner = models.CharField(max_length=3, null=True , blank=True ,choices=Answer_choices)
    SeriousSkinRepair = models.CharField(max_length=3, null=True , blank=True ,choices=Answer_choices)
    Preagnant = models.CharField(max_length=3, null=True , blank=True,choices=Answer_choices)
    Abortion = models.CharField(max_length=3, null=True , blank=True,choices=Answer_choices)
    BreastFeeding = models.CharField(max_length=3, null=True , blank=True,choices=Answer_choices)
    BloodHealthfulnessInfo = models.CharField(max_length=10, null=True , blank=True,choices=Answer_choices)
    Status = models.CharField(null=True , max_length=11 , blank=True , default='in progress')
    Request_time = models.TimeField(auto_now_add=True , null=True , blank=True)
    Request_Date = models.DateField(auto_now_add=True  , null=True , blank=True)
    class Meta:
        db_table = "DonationRequestFormResult"


   





