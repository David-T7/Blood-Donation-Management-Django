from django.forms import ModelForm
from .models import Blood
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class BloodCreationForm(ModelForm):
    class Meta:
        model = Blood
        fields = ['BloodGroup','PackNo','ExpDate','QuantityOfBlood']
        widgets = {
            'ExpDate':DateInput(),
        } 
    