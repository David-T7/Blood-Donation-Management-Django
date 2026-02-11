from datetime import datetime, timezone, timedelta
from datetime import date
from django.shortcuts import redirect, render
from Donor.models import Appointment, Donor
from LabTechnician.models import FininshedAppointment
from .models import Blood , BloodHistory
from UserAccount.models import UserRegistration
from .forms import BloodCreationForm
from django.contrib import  messages
from Donor.models import Appointment
from django.utils.dateparse import parse_date 


def UserState(request):
    user = request.user
    account = UserRegistration.objects.get(Account_id=user.id)
    context={'account':account}
    return context


def BloodStock(request):
    account = UserState(request)['account']
    dic={'O+':0,'B+':0,'A+':0,'AB+':0,'O-':0,'B-':0,'A-':0,'AB-':0,}
    for i in Blood.objects.all():
        dic[i.BloodGroup]+=int(i.QuantityOfBlood)
    context = {
        'account':account,
        'Op':dic['O+'],'Ap':dic['A+'],'Bp':dic['B+'],'ABp':dic['AB+'],
        'Om':dic['O-'],'Am':dic['A-'],'Bm':dic['B-'],'ABm':dic['AB-'], 
        'active_page':'blood',
    }
    return render(request ,'bbmanager/bloodstock.html' , context)

def AddBlood(request , pk , pk2):
    donor = Donor.objects.get(Donor_id = pk)
    account = UserState(request)['account']
    form = BloodCreationForm(initial={'BloodGroup': donor.Bloodgroup})
    if request.method == 'POST':
        form= BloodCreationForm(request.POST)
        if (form.is_valid()):
            try:
                blood = form.save(commit=False)
                blood.Donor_id = donor
                blood.save()
                BloodHistory.objects.create(Blood_id=blood ,Action='Added') 
                appointment = Appointment.objects.get(App_id = pk2)
                FininshedAppointment.objects.create(Appointment_id = appointment)
                messages.success(request, 'Successfully added blood')
                return redirect('/labdonationrequest/notall')
            except:
                messages.error(request, 'Error during adding blood')
        else: 
            messages.error(request, 'Error during adding blood form')
    context = {'form':form , 'account':account ,   'active_page':'blood', 'blood_type':str(donor.Bloodgroup)}
    return render (request , 'labtechnician/addblood.html' , context)


def GetBlood(request , type):
    account = UserState(request)['account']
    three_days_after = None
    bloods = None
    try:
        if(type=='all'):
            bloods = Blood.objects.all()
        elif(type=='notall'):
            bloods = Blood.objects.all()[0:5]
        elif(type=='searched'):
            print('in searched')
            if request.method == 'POST':
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'BloodType'):
                    print('by blood type')
                    bloods = Blood.objects.filter( BloodGroup =  searched)
                elif(searchby == 'Volume'):
                    print('in volume')
                    bloods = Blood.objects.filter( QuantityOfBlood =  searched) 
                elif(searchby == 'ExpirationDate'):
                    expdate = parse_date(searched)
                    bloods = Blood.objects.filter(ExpDate =  expdate) 
                elif(searchby == 'Expired'):
                    print('in expired')
                    today = date.today()
                    bloods = Blood.objects.filter(ExpDate__lte = today) 
    except:
        bloods = None
    try:
        three_days_after = date.today() +  datetime.timedelta(days=3)
    except:
        three_days_after = None
    context = {'account': account , 'type':type ,  'bloods':bloods , 'threedaysafter':three_days_after ,   'active_page':'blood', }
    return render(request , 'labtechnician/bloods.html' , context)


  
def UpdateBlood(request , pk ):
    account = UserState(request)['account']
    blood = None
    try:
        blood = Blood.objects.get(Blood_id=pk)
        form = BloodCreationForm(instance=blood)
    except:
        blood =None
        form = BloodCreationForm()
    if request.method == 'POST':
        form = BloodCreationForm(request.POST, instance=blood)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blood was updated successfully!')
            return redirect('/getlabbloods/notall') 
        else:
            messages.success(request, 'event was not updated successfully!')
    context = {'form': form ,'type':'update' ,  'account':account ,   'active_page':'blood',}
    return render(request, 'labtechnician/addblood.html', context)


def DeleteBlood(request , pk):
    account = UserState(request)['account']
    blood = None
    try:
        blood = Blood.objects.get(Blood_id=pk)
        blood.delete()
        messages.success(request, 'Blood was deleted successfully!')
    except:
        messages.success(request, 'Blood was not  deleted successfully!')
    context = { 'account':account ,   'active_page':'blood',}
    return render(request, 'labtechnician/bloods.html', context)

        
from datetime import datetime, timezone, timedelta
from datetime import date

def BloodsHistory(request, type):
    account = UserState(request)['account']
    
    # Get queryset based on type, ordered by Blood registration date
    if type == 'all':
        blood_history_queryset = BloodHistory.objects.select_related('Blood_id').order_by('-Blood_id__RegDate')
    elif type == 'notall':
        blood_history_queryset = BloodHistory.objects.select_related('Blood_id').order_by('-Blood_id__RegDate')[:5]
    elif type == 'searched' and request.method == 'POST':
        searchby = request.POST.get('searchby', '')
        searched = request.POST.get('searched', '')
        
        if searchby == 'BloodType':
            blood_history_queryset = BloodHistory.objects.filter(
                Blood_id__BloodGroup__icontains=searched
            ).select_related('Blood_id').order_by('-Blood_id__RegDate')
        elif searchby == 'Volume':
            blood_history_queryset = BloodHistory.objects.filter(
                Blood_id__QuantityOfBlood__icontains=searched
            ).select_related('Blood_id').order_by('-Blood_id__RegDate')
        elif searchby == 'ExpirationDate':
            blood_history_queryset = BloodHistory.objects.filter(
                Blood_id__ExpDate__icontains=searched
            ).select_related('Blood_id').order_by('-Blood_id__RegDate')
        elif searchby == 'RegistrationDate':
            blood_history_queryset = BloodHistory.objects.filter(
                Blood_id__RegDate__icontains=searched
            ).select_related('Blood_id').order_by('-Blood_id__RegDate')
        elif searchby == 'Action':
            blood_history_queryset = BloodHistory.objects.filter(
                Action__icontains=searched
            ).select_related('Blood_id').order_by('-Blood_id__RegDate')
        else:
            blood_history_queryset = BloodHistory.objects.none()
    else:
        blood_history_queryset = BloodHistory.objects.none()
    
    # Add expiry status to each history item
    today = date.today()
    for history in blood_history_queryset:
        if hasattr(history, 'Blood_id') and history.Blood_id:
            exp_date = history.Blood_id.ExpDate
            if isinstance(exp_date, str):
                # Parse string date if needed
                try:
                    exp_date = datetime.strptime(exp_date, '%Y-%m-%d').date()
                except ValueError:
                    exp_date = None
            
            if exp_date:
                days_until_expiry = (exp_date - today).days
                
                if days_until_expiry < 0:
                    history.expiry_status = 'expired'  # Already expired
                elif days_until_expiry <= 3:
                    history.expiry_status = 'critical'  # Critical - expires soon
                else:
                    history.expiry_status = 'safe'  # Safe - not close to expiry
    
    # Prepare context
    context = {
        'account': account,
        'bloods': blood_history_queryset,
        'type': type,  # Pass the type to the template for button logic
        'active_page': 'blood',
    }
    
    return render(request, 'bbmanager/seebloodhistory.html', context)










                

    




