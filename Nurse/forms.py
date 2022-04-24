from django.forms import ModelForm
from django import forms
from Nurse.models import AppointmentChoice

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'


class AppointmentChoiceCreationForm(ModelForm):
    class Meta:
        model = AppointmentChoice
        fields = ['Date','Time']
        widgets = {
            'Date': DateInput(),
            'Time': TimeInput()
        } 