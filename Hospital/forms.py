from django import forms
from django.forms import ModelForm
from UserAccount.models import Account
from .models import Hospital , BloodRequest
from django.contrib.auth.forms import UserCreationForm

class HospitalCreationForm(ModelForm):
    class Meta:
        model = Hospital
        fields = ['HospitalName' , 'BranchNo' , 'HospitalRepresentative','Username','ProfilePic']



class BloodRequestForm(ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['Blood_Group' , 'Quantity']
        def __init__(self, *args, **kwargs):
            super(BloodRequestForm, self).__init__(*args, **kwargs)

            for field_name, field in self.fields.items():
                if(field.label == 'Quantity'):
                    self.fields[field_name].widget.attrs['placeholder'] = '0ML'

        Quantity = forms.CharField(widget= forms.TextInput
                           (attrs={'placeholder':'Enter your first name'}))
class hopsitalProfilePictureForm(ModelForm):
    class Meta:
        model = Hospital
        fields = ['ProfilePic']


