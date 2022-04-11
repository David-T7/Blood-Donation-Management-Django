from django.views import View
from Event.models import Camp
from . import views
from django.urls import path
from .views import Camps
urlpatterns = [
path('camps/', views.Camps, name='camps'),
path('events/<type>', views.Events, name='events'),
path('addevent',views.CreateEvent , name='addevent'), 
path('addcamp',views.CreateCamp , name='addcamp'), 
path('updateevent/<pk>' , views.UpdateEvent , name='updateevent'),
path('deleteevent/<pk>' , views.DeleteEvent , name='deleteevent'),
]