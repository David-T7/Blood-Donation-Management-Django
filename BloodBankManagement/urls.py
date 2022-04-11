from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('UserAccount.urls')),
    path('',include('Event.urls')),
    path('',include('Blood.urls')),
    path('',include('BBManager.urls')),
    path('',include('Nurse.urls')),
    path('',include('Hospital.urls')),
    path('',include('Donor.urls')),
    path('',include('LabTechnician.urls')),
    path('admin/', admin.site.urls , name='admin'),
]
