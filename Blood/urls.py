from Blood.models import Blood
from . import views
from django.urls import path
urlpatterns = [
path('bloodstock/',  views.BloodStock, name='bloodstock'),
path('addblood/<pk>/<pk2>' , views.AddBlood , name = 'addblood'),
path('updateblood/<pk>' , views.UpdateBlood , name = 'updateblood'),
path('deleteblood/<pk>' , views.DeleteBlood , name = 'deleteblood'),
path('seebloodhistory<type>' , views.BloodsHistory , name='bloodhistory'),
path('getlabbloods/<type>'  , views.GetBlood , name='getlabbloods' ),

]