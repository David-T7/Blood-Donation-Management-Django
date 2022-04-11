from . import views
from django.urls import path
from .views import BBDashbord, BBmanager

urlpatterns = [
path('bbmanager',views.BBmanager, name='bbmanager'),
path('bbdashbord/<type>',views.BBDashbord , name='bbdashbord'),
]

