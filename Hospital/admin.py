from django.contrib import admin

from Hospital.models import BloodRequest, Hospital, HospitalSentBloods

# Register your models here.
admin.site.register(BloodRequest)
admin.site.register(Hospital)
admin.site.register(HospitalSentBloods)