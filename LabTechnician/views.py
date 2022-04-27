from multiprocessing import context
from django.contrib import  messages
import itertools
from django.shortcuts import redirect, render
from Blood.forms import BloodCreationForm
from Blood.models import Blood
from Donor.models import Appointment, DonationRequestFormResult, Donor
from LabTechnician.models import FininshedAppointment , DeferringList
from UserAccount.models import Account, Address, UserRegistration
from django.utils.dateparse import parse_date 


def UserState(request):
    user = request.user
    account = UserRegistration.objects.get(Account_id=user.id)
    context={'account':account}
    return context


def LabTechnician(request):
    account = UserState(request)['account']
    context = {'user': request.user  , 'account':account}
    return render(request , 'labtechnician/labtechnician.html' , context)

def DonationRequest(request ,  type):
    account = UserState(request)['account']
    donation = None
    appointment = None
    finished_appointment = []
    deferringlist = []
    try:
        for fa in FininshedAppointment.objects.all():
            finished_appointment.append(str(fa.Appointment_id))
    except:
        finished_appointment=[]
    try:
        if(type=='all'):
            donation = DonationRequestFormResult.objects.all()
        elif(type=='notall'):
            donation = DonationRequestFormResult.objects.all()[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                print('in post')
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'RequestDate'):
                    date = parse_date(searched)
                    donation = DonationRequestFormResult.objects.filter(Request_Date =  date)
                elif(searchby == 'AppointmentDate'):
                    date = parse_date(searched)
                    app = Appointment.objects.filter(Date = date)
                    donation = DonationRequestFormResult.objects.filter(Donor_id = app[0].Donor_id)
                elif(searchby == 'DonorName'):
                    dn = Donor.objects.filter(Donorname = searched)
                    donation = DonationRequestFormResult.objects.filter(Donor_id = str(dn[0].Donor_id))
                elif(searchby == 'Phone'):
                    addr = Address.objects.get(Phone = int(searched))
                    dn = Donor.objects.filter(Address_id = addr)
                    donation = DonationRequestFormResult.objects.filter(Donor_id = str(dn[0].Donor_id))
                elif(searchby == 'AppointmentStatus'):
                    app = Appointment.objects.filter(status =  searched)
                    donation = DonationRequestFormResult.objects.filter(Donor_id = str(app[0].Donor_id))

    except:
        donation = None
    try:
        if(type=='all'):
            appointment = Appointment.objects.all()
        elif(type=='notall'):
            appointment = Appointment.objects.all()[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                searchby = request.POST['searchby']
                searched = request.POST['searched']
            if(searchby == 'AppointmentDate'):
                date = parse_date(searched)
                appointment = Appointment.objects.filter(Date = date)
            elif(searchby == 'DonorName'):
                appointment = Appointment.objects.filter(Donor_id = donation[0].Donor_id)
            elif(searchby == 'Phone'):
                appointment = Appointment.objects.filter(Donor_id = donation[0].Donor_id)
            elif(searchby == 'AppointmentStatus'):
                appointment = Appointment.objects.filter(status =  searched)
            elif(searchby == 'RequestDate'):
                appointment = Appointment.objects.filter(Donor_id = donation[0].Donor_id)
    except:
        appointment = None
    try:
        for dl in DeferringList.objects.all():
            deferringlist.append(str(dl.Donor_id))
    except:
        deferringlist = []
    my_list=[]
    try:
        my_list = list(itertools.zip_longest(donation,appointment))
    except:
        my_list = []
    context = {'list':my_list , 'donation':donation ,'account':account , 'finished':finished_appointment , 'deferringlist':deferringlist }
    return render (request , 'labtechnician/donationrequest.html' , context  )

def BlockDonor(request , donor_id):
    donor = Donor.objects.get(Donor_id = donor_id)
    try:
        DeferringList.objects.create(Donor_id = donor)
        messages.success(request,'Donor was Succesfuly Added to DeferingList')
        return redirect('/labdonationrequest/notall')
    except:
        messages.error(request,'Donor was not Successfuly Added to DeferingList')
        return redirect('/labdonationrequest/notall')

def UnblockDonor(request , donor_id):
    
    donor = Donor.objects.get(Donor_id = donor_id)
    try:
        list = DeferringList.objects.get(Donor_id = donor)
        list.delete()
        messages.success(request,'Donor was Succesfuly removed from DefefringList')
        return redirect('/labdonationrequest/notall')
    except:
        messages.error(request,'Donor was not Successfuly removed form DefefringList ')
        return redirect('/labdonationrequest/notall')

def GetDonorAddress(request , pk):
    account = UserState(request)['account']
    address = None
    acc = None
    try:
            acc = Donor.objects.get(Donor_id = pk)
    except:
            acc = None
    try:
        address = Address.objects.get(Address_id = str(acc.Address_id))
    except:
        address= None
    context = {'account': account , 'address':address , 'donor':acc }
    return render(request , 'labtechnician/checkdonor.html' , context)

def GetBlood(request , type):
    account = UserState(request)['account']
    bloods = None
    try:
        if(type=='all'):
            bloods = Blood.objects.all()
        elif(type=='notall'):
            bloods = Blood.objects.all()[0:5]
    except:
        bloods = None
    context = {'account': account , 'bloods':bloods }
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
            return redirect('/labdonationrequest/notall')
        else:
            messages.success(request, 'event was not updated successfully!')
    context = {'form': form ,'type':'update' ,  'account':account}
    return render(request, 'bbmanager/addblood.html', context)


def DeleteBlood(request , pk):
    account = UserState(request)['account']
    blood = None
    try:
        blood = Blood.objects.get(Blood_id=pk)
        blood.delete()
        messages.success(request, 'Blood was deleted successfully!')
    except:
        messages.success(request, 'Blood was not  deleted successfully!')
    context = { 'account':account}
    return render(request, 'bbmanager/addblood.html', context)
    





            





    
        









