from django import forms
from django.forms import ModelForm
from UserAccount.models import Account
from .models import Hospital , BloodRequest
from django.contrib.auth.forms import UserCreationForm

class HospitalCreationForm(ModelForm):
    class Meta:
        model = Hospital
        fields = ['HospitalName' , 'BranchNo' , 'HospitalRepresentative','ProfilePic']



class BloodRequestForm(ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['Blood_Group' , 'Quantity']
class hopsitalProfilePictureForm(ModelForm):
    class Meta:
        model = Hospital
        fields = ['ProfilePic']


