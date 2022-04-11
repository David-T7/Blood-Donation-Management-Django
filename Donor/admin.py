from django.contrib import admin
from .models import Appointment, Donor , DonationRequestFormQuesitons , DonationRequestFormResult
# Register your models here.
admin.site.register(DonationRequestFormResult )
admin.site.register(Appointment)