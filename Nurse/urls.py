from . import views
from django.urls import path
urlpatterns = [
path('nurse',views.Nurse, name='nurse'),
path('donorrequest/<type>', views.DonationRequest , name='donorrequest'),
path('checkrequest/<uuid:pk>' , views.CheckRequest , name='checkrequest'),
path('checkappointment/<type>', views.CheckAppointments , name='checkappointment'),
path('donorquestions/<type>', views.DonorQuestions , name='donorquestions'),
path('donoraddress/<uuid:pk>/<sender>' , views.GetDonorAddress , name='donoraddress'),
path('addquestions/<type>',views.AddQuestions , name='addquestions'),
# path('appointmentchoices/<type>', views.AppointmentChoices , name='appointmentchoices'),
# path('addappointment/<type>',views.AddAppointmentDate , name='addappointmentchoice'),
path('updatequestion/<uuid:pk>' , views.UpdateQuestion , name='updatequestion'),
# path('updateappointmentchoice/<uuid:pk>' , views.UpdateAppointmentChoice , name='updateappointmentchoice'),
# path('deleteappointmentchoice/<uuid:pk>' , views.DeleteAppointmentChoice , name='deleteappointmentchoice'),
path('deletequestion/<uuid:pk>' , views.DeleteQuestion , name='deletequestion'),
path('confirmrequest/<uuid:pk>/<type>' , views.Confirmrequest , name='confirmrequest'),
path('confirmappointemnt/<uuid:pk>/<type>' , views.confirmappointment , name='confirmappointment'),
]