from django.shortcuts import redirect, render
from Donor.models import Appointment, Donor
from LabTechnician.models import FininshedAppointment
from .models import Blood , BloodHistory
from UserAccount.models import UserRegistration
from .forms import BloodCreationForm
from django.contrib import  messages
from Donor.models import Appointment

def UserState(request):
    user = request.user
    account = UserRegistration.objects.get(Account_id=user.id)
    context={'account':account}
    return context


def BloodStock(request):
    account = UserState(request)['account']
    dic={'O+':0,'B+':0,'A+':0,'AB+':0,'O-':0,'B-':0,'A-':0,'AB-':0,}
    for i in Blood.objects.all():
        dic[i.BloodGroup]+=int(i.QuantityOfBlood[:-2])
    context = {
        'account':account,
        'Op':dic['O+'],'Ap':dic['A+'],'Bp':dic['B+'],'ABp':dic['AB+'],
        'Om':dic['O-'],'Am':dic['A-'],'Bm':dic['B-'],'ABm':dic['AB-'], 
    }
    return render(request ,'bbmanager/bloodstock.html' , context)

def AddBlood(request , pk , pk2):
    donor = Donor.objects.get(Donor_id = pk)
    account = UserState(request)['account']
    form = BloodCreationForm()
    if request.method == 'POST':
        form= BloodCreationForm(request.POST)
        if (form.is_valid()):
            try:
                blood = form.save(commit=False)
                blood.Donor_id = donor
                blood.save()
                BloodHistory.objects.create(Blood_id=blood.Blood_id , Donor_id = donor.Donor_id ,BloodGroup = blood.BloodGroup , 
                PackNo = blood.PackNo , RegDate = blood.RegDate , ExpDate = blood.ExpDate , QuantityOfBlood = blood.QuantityOfBlood , Action='Added'      ) 
                appointment = Appointment.objects.get(App_id = pk2)
                FininshedAppointment.objects.create(Appointment_id = appointment)
                messages.success(request, 'Successfully added blood')
                return redirect('/labdonationrequest/notall')
            except:
                messages.error(request, 'Error during adding blood')
        else: 
            messages.error(request, 'Error during adding blood form')
    context = {'form':form , 'account':account}
    return render (request , 'labtechnician/addblood.html' , context)
        
def BloodsHistory(request , type):
    account = UserState(request)['account']
    bloods = None
    try:
        if(type == 'all'):
            bloods = BloodHistory.objects.all()[::-1]
        else:
            bloods = BloodHistory.objects.all()[0:5][::-1]   
    except:
        bloods = None
    context = {'account':account , 'bloods':bloods}
    return render (request , 'bbmanager/seebloodhistory.html' , context)







                

    




