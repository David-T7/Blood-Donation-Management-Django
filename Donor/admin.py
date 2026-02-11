from django.contrib import admin
from .models import Appointment, Donor , DonationRequestFormQuesitons , DonationRequestFormResult, DonationRequestQuestion, DonationRequestAnswer

# Register your models here.
admin.site.register(DonationRequestFormResult )
admin.site.register(Appointment)
admin.site.register(Donor)
admin.site.register(DonationRequestQuestion)
admin.site.register(DonationRequestAnswer)