from . import views
from django.urls import path
from .views import  HomePage , AboutUs

urlpatterns = [
path('',  HomePage.as_view(), name='homepage'),
path('aboutus', AboutUs.as_view() , name='aboutus'), 
path('login/<role>', views.Login , name='login'),
path('logout' , views.Logout , name='logout') , 
path('reset/<role>',views.ResetPassword , name='reset'),
path('forgot/<role>',views.ForgotPassword , name='forgot'),
path('editusername' , views.EditUserName , name='editusername'  ),
path('editpassword' , views.EditPassword , name='editpassword'),
path('editprofilepicture' , views.EditProfilePicture , name='editprofilepicture'),
]