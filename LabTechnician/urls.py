from . import views
from django.urls import path
urlpatterns = [
path('labtechnician/', views.LabTechnician, name='labtechnician'),
path('labdonationrequest/<type>' , views.DonationRequest , name='labdonationrequest'),
path('blockdonor/<donor_id>' , views.BlockDonor , name='blockdonor'),
path('unblockdonor/<donor_id>' , views.UnblockDonor , name='unblockdonor'),
path('labdonorinfo/<str:pk>' , views.GetDonorAddress , name='labdonorinfo'),
]