from multiprocessing import context
from django.contrib import  messages
import itertools
from django.shortcuts import redirect, render
from Blood.models import Blood
from Donor.models import Appointment, DonationRequestFormResult, Donor
from LabTechnician.models import FininshedAppointment , DeferringList
from UserAccount.models import Address, UserRegistration

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
        else:
            donation = DonationRequestFormResult.objects.all()[0:5]
    except:
        donation = None
    try:
        if(type=='all'):
            appointment = Appointment.objects.all()
        else:
            appointment = Appointment.objects.all()[0:5]
    except:
        appointment = None
    try:
        for dl in DeferringList.objects.all():
            deferringlist.append(str(dl.Donor_id))
    except:
        deferringlist = []
    my_list = list(itertools.zip_longest(donation,appointment))
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


    
        









