from . import views
from django.urls import path
urlpatterns = [
path('nurse',views.Nurse, name='nurse'),
path('donorrequest/<type>', views.DonationRequest , name='donorrequest'),
path('checkrequest/<pk>' , views.CheckRequest , name='checkrequest'),
path('checkappointment/<type>', views.CheckAppointments , name='checkappointment'),
path('donorquestions/<type>', views.DonorQuestions , name='donorquestions'),
path('donoraddress/<pk>' , views.GetDonorAddress , name='donoraddress'),
path('addquestions/<type>',views.AddQuestions , name='addquestions'),
path('updatequestion/<pk>' , views.UpdateQuestion , name='updatequestion'),
path('deletequestion/<pk>' , views.DeleteQuestion , name='deletequestion'),
path('confirmrequest/<pk>/<type>' , views.Confirmrequest , name='confirmrequest'),
path('confirmappointemnt/<pk>/<type>' , views.confirmappointment , name='confirmappointment'),
]