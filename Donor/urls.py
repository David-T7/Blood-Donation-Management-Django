from . import views
from django.urls import path
urlpatterns = [
path('donor/', views.Donors, name='donor'),
path('register',views.Register , name='register'),
path('donordashbord/<type>' , views.DonorDashbord , name='donordashbord'),
path('donationrequest/<type>' , views.DonationRequest , name='donationrequest'),
path('makerequest', views.MakeDonationRequest , name='makerequest'),
path('cancelrequest/<pk>' , views.CancelRequest , name='cancelrequest'),
path('updaterequest/<pk>' , views.UpdateRequest , name='updaterequest'),
path('makeappointment', views.MakeAppointment , name='makeappointment'),
path('getappointments/<type>' , views.GetAppointments , name='getappointments'),
path('cancelappointment/<pk>' , views.CancelAppointment , name='cancelappointment'),
path('updateappointment/<pk>/' , views.UpdateAppointment , name='updateappointment'),
# path('donappointmentchoices/<type>/<sender>/<pk>', views.AppointmentChoices , name='donappointmentchoices'),
path('getevent/<type>' , views.GetEvent , name='getevent'),
path('getcamps/<type>'  , views.Camps , name='getcamps' ),
path('seecamp/<pk>' , views.SeeCamp , name='seecamp' ),
# path('donoreditusername' , views.EditUserName , name='donoreditusername'),
# path('donoreditpassword' , views.EditPassword , name='donoreditpassword'),
# path('donoreditprofilepicture' , views.EditProfile ,name= 'donoreditprofilepicture'),
]