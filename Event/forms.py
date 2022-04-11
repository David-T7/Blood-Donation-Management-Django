from django import forms
from django.forms import ModelForm
from .models import Event , Camp

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'

class EventCreationForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'EventTime': TimeInput(),
            'EventDate': DateInput(),
        }

class CampCreationForm(ModelForm):
    class Meta:
        model = Camp
        fields = '__all__'