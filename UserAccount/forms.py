from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Account, Address, UserRegistration
from django.forms import ModelForm
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
