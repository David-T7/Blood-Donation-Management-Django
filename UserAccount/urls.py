from . import views
from django.urls import path
from .views import  HomePage

urlpatterns = [
path('',  HomePage.as_view(), name='homepage'), 
path('login/<role>', views.Login , name='login'),
path('logout' , views.Logout , name='logout') , 
path('reset/<role>',views.ResetPassword , name='reset'),
path('forgot/<role>',views.ForgotPassword , name='forgot'),
path('editusername' , views.EditUserName , name='editusername'  ),
path('editpassword' , views.EditPassword , name='editpassword'),
path('eidtprofilepicture' , views.EditProfilePicture , name='editprofielpicture'),
]