from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account, Address, UserRegistration
from django.forms import ModelForm
from .models import Account
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm,
                                       PasswordResetForm,
                                       SetPasswordForm
                                       )
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Account
        fields = UserCreationForm.Meta.fields + ('Role',)
class CusotmUserRegisteration(ModelForm):
    class Meta:
        model = UserRegistration
        fields = '__all__'
class ProfilePictureUpdateForm(ModelForm):
    class Meta:
        model = UserRegistration
        fields = ['ProfilePic']
class CustomUserChangeForm(ModelForm):
    class Meta:
        model = Account
        fields = ['username']
class AddressCreationForm(ModelForm):
     class Meta:
        model = Address
        fields = '__all__'







class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "input",
        "type": "email",
        "placeholder": "enter email-id"
    }))


class NewPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(NewPasswordForm, self).__init__(*args, **kwargs)

    
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': "input",
            "type": "password",
            'autocomplete': 'new-password'
    }))

    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': "input",
            "type": "password",
            'autocomplete': 'new-password'
    }))


