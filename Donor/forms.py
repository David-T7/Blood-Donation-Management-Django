from django import forms
from django.forms import ModelForm
from .models import Donor , Appointment , DonationRequestFormResult, DonationRequestQuestion, DonationRequestAnswer

class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'
class DateTimeInput(forms.DateTimeInput):
    input_type = 'date'

class DonorCreationForm(ModelForm):
    class Meta:
        model = Donor
        fields = ['Donorname','DateOfBirth','Bloodgroup','Gender','Nationality','Height','Weight','BloodPressure']
        widgets = {
            'DateOfBirth': DateInput(),
        }
class DonorAccountEditForm(ModelForm):
    class Meta:
        model = Donor
        fields = ['ProfilePic']



class AppointmentCreationForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['Date','Time']
        widgets = {
            'Time': TimeInput(),
            'Date': DateInput(),
        }

class RequestAnswerCreationForm(ModelForm):
    class Meta:
        model = DonationRequestFormResult
        fields = []

class DynamicDonationRequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.donor = kwargs.pop('donor', None)
        super().__init__(*args, **kwargs)

        # Get all active questions
        questions = DonationRequestQuestion.objects.all()

        # Add fields for each question
        for question in questions:
            # Skip gender-specific questions if donor is not of required gender
            if question.is_gender_specific and self.donor and self.donor.Gender != question.gender_required:
                continue

            self.fields[f'question_{question.question_id}'] = forms.ChoiceField(
                choices=[('', 'Select an option'), ('yes', 'Yes'), ('no', 'No')],
                label=question.question_text,
                widget=forms.Select(attrs={'class': 'form-select'})
            )

class DonationRequestQuestionForm(ModelForm):
    class Meta:
        model = DonationRequestQuestion
        fields = '__all__'