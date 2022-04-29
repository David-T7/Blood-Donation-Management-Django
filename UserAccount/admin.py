from django.contrib import admin
from .models import Address,Account, UserRegistration
from django.contrib.auth.admin import UserAdmin
from .forms import  CustomUserCreationForm
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = Account
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','password1', 'password2','Role','email')}
        ),
    )
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','password','Role','email')}
        ),
    )
    
admin.site.register(UserRegistration)
admin.site.register(Account , CustomUserAdmin)
admin.site.register(Address)

