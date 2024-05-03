from Hospital.models import Hospital
from . import views
from django.urls import path
from .views import HospitalRequest  ,Hospitals
urlpatterns = [
path('hospitalrequest/<type>', views.HospitalRequest, name='hospitalrequest'), 
path('hospitals/<type>' , views.Hospitals , name='hospitals'),
# path('addhospital' , views.AddHospital , name='addhospital'),
path('updatehospital/<pk>' , views.UpdateHospital , name='updatehospital'),
path('deletehospital/<pk>' , views.DeleteHospital , name='deletehospital'),
path('hospitalrep' , views.HospitalRep , name='hospitalrep'),
path('hospitaldashbord/<type>' , views.HospitalDashbord , name='hospitaldashbord'),
path('MakeBloodRequest' , views.MakeBloodRequest , name = 'makebloodrequest'),
path('bloodrequest/<type>' , views.BloodRequests  ,name='bloodrequest'),
path('edithospitalprofielpicture' , views.EditHospitalProfilePicture , name='edithospitalprofile' ),
path('edithospitalusername' , views.EditUserName , name='edithospitalusername'),
path('edithospitalaccount' , views.EditHospitalAccount , name='edithospitalaccount'),
path('hospitaladdress/<pk>' , views.GetHopsitalAddress , name='hospitaladdress'),
path('acceptbloodrequest/<pk>/<type>' , views.AcceptBloodRequest , name='acceptbloodrequest'),
]