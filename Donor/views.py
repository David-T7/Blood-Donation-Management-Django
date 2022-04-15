import imp
import itertools
from multiprocessing import context
from django.contrib import  messages
from django.shortcuts import redirect, render
from Donor.forms import AppointmentCreationForm, DonorCreationForm , DonationRequestFormQuesitons, DonorAccountEditForm , RequestAnswerCreationForm
from Donor.models import Appointment, Donor 
from UserAccount.models import Account , Address
from UserAccount.forms import AddressCreationForm, CustomUserCreationForm , CustomUserChangeForm
from Donor.models import DonationRequestFormResult , DonationRequestFormQuesitons 
from Event.models import Event
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from LabTechnician.models import DeferringList

def Register(request):
    form1 = DonorCreationForm()   # using the donor creation form created in forms.py
    form2= AddressCreationForm()
    form3= CustomUserCreationForm()
    if request.method == 'POST':
        form1= DonorCreationForm(request.POST)  # getting values send from the page
        form2= AddressCreationForm(request.POST)
        form3 = CustomUserCreationForm(request.POST)
        if (form1.is_valid() and form2.is_valid() and form3.is_valid()):  # checking  values send from the page are valid  
            try:
                account = form3.save(commit=False) # saving the values but not in the table
                account.Role='Donor'
                account.save() # saving the user account
                address = form2.save(commit=False)
                address.save()
                donor = form1.save(commit=False)
                phone = request.POST['Phone']
                donor.Address_id= Address.objects.get(Phone=phone)  # assingnin donor_id field in donor form adress table using phone
                donor.Account_id = account
                donor.save()
                messages.success(request, 'Successfully Registered')
                return redirect('/login/Donor')
            except:   
                messages.error(request, 'An error has occurred during registration after form')
        else:
            messages.error(
                request, 'An error has occurred during registration')
    context = {'form1': form1,'form2':form2,'form3':form3}  # forms that are passed to the page rendered
    return render(request, 'register1.html',context)


def DonorState(request):
    donor = request.user
    context = {'donor': Donor.objects.get(Account_id = donor.id) }
    return context

def Donors(request):
    context = {'user':request.user , 'donor':DonorState(request)['donor']}
    return render(request , 'donor/donor.html' , context)

def EditAccount(request):
    state = request.user
    useraccount = Account.objects.get(id=state.id)
    donor= Donor.objects.get(Account_id = useraccount.id)
    form1= CustomUserChangeForm(instance= state)
    form2= DonorAccountEditForm (instance=donor)
    form3 = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form1 = CustomUserChangeForm(request.POST, instance=state)
        form2 = DonorAccountEditForm(request.POST, request.FILES, instance=donor)
        form3 = PasswordChangeForm(request.user, request.POST)

        if (form1.is_valid() and form2.is_valid() and form3.is_valid()):
            try:
                user = form3.save()
                update_session_auth_hash(request, user)
            except:
                messages.error(request,'Error occured during updating password')
            try:
                form1.save()
                messages.success(request,'Account updated successfuly')
            except:
                messages.error(request,'Error occured during updating account')
            try:
                form2.save()
            except:
                messages.error(request,'Error occured during updating profile pic')
        else:
                messages.error(request,'please input correct information')
        request.user.save()
    context = {'form1': form1 , 'form2':form2 ,'form3':form3 , 'donor':donor }
    return render(request, 'donor/editaccount.html', context)

    
def DonorDashbord(request , type):
    donor = DonorState(request)['donor']
    donationrequest_no = 0
    accepted_no = 0
    pending_no = 0
    rejected_no = 0
    donation = None
    appointment = None
    try:
        if(type=='all'):
            donation = DonationRequestFormResult.objects.filter(Donor_id = donor.Donor_id)
        else:
            donation = DonationRequestFormResult.objects.filter(Donor_id = donor.Donor_id)[0:5]
    except:
        done = None
    try:
        if(type=='all'):
            appointment = Appointment.objects.filter(Donor_id = str(donor.Donor_id))
        else:
            appointment = Appointment.objects.filter(Donor_id = str(donor.Donor_id))[0:5]
    except:
        print('no appointment')
        appointment = None
    try:
        donationrequest_no = len(DonationRequestFormResult.objects.filter(Donor_id = donor.Donor_id))
    except:
        donationrequest_no=0
    try:
        accepted_no = len( DonationRequestFormResult.objects.filter(Status = 'accepted').filter(Donor_id = donor.Donor_id))
    except:
        accepted_no = 0
    try:
        pending_no = len( DonationRequestFormResult.objects.filter(Status = 'in progress').filter(Donor_id = donor.Donor_id))
    except:
        pending_no = 0
    try:
        rejected_no = len( DonationRequestFormResult.objects.filter(Status = 'rejected').filter(Donor_id = donor.Donor_id))
    except:
        rejected_no = 0
    my_list = list(itertools.zip_longest(donation,appointment))
    context={'request_no': donationrequest_no ,
            'accepted_no': accepted_no,
            'pending_no':pending_no,
            'rejected_no':rejected_no ,
            'donation':donation,
            'donor':donor,
            'list':my_list,
    }
    return render(request, 'donor/dashbord.html' ,context)

def DonationRequest(request , type):
    donor = DonorState(request)['donor']
    donation = None
    appointment = None
    try:
        if(type=='all'):
            donation = DonationRequestFormResult.objects.filter(Donor_id = donor.Donor_id)
        else:
            donation = DonationRequestFormResult.objects.filter(Donor_id = donor.Donor_id)[0:5]
    except:
        donation = None
    try:
        if(type=='all'):
            appointment = Appointment.objects.filter(Donor_id = str(donor.Donor_id))
        else:
            appointment = Appointment.objects.filter(Donor_id = str(donor.Donor_id))[0:5]
    except:
        print('no appointment')
        appointment = None
    my_list = list(itertools.zip_longest(donation,appointment))
    context = {'list':my_list , 'donation':donation , 'donor':donor}
    return render (request , 'donor/donationrequest.html' , context  )

def MakeDonationRequest(request):
    donor = DonorState(request)['donor']
    form = RequestAnswerCreationForm()
    questions = None
    deferringList = None
    try:
        questions = DonationRequestFormQuesitons.objects.all()[0]
    except:
        questions = None
    try:
        deferringList =  DeferringList.objects.get(Donor_id = donor)
    except:
        deferringList = None
        print('list not found')
    if request.method == 'POST':
        form= RequestAnswerCreationForm(request.POST)
        if (form.is_valid()):
            try:
                req = form.save(commit=False)
                req.Donor_id = donor
                if(deferringList):
                    req.Status = 'rejected'
                    messages.error(request , 'Sorry you cant make a donation because of health issues')
                    req.save()
                else:
                    req.save()
                    messages.success(request , 'request sent successfuly')
                return redirect('/donationrequest/notall')
            except:
                messages.success(request , 'error during request')
        else:
            messages.success(request , 'request was not successful')
    
    context = { 'form':form , 'questions':questions , 'donor':donor}
    return render(request, 'donor/createdonationrequest.html',context)                   


def MakeAppointment(request):
    donor = DonorState(request)['donor']
    form = AppointmentCreationForm()
    if request.method == 'POST':
        form= AppointmentCreationForm(request.POST)
        if (form.is_valid()):
            try:
                appointment = form.save(commit=False)
                appointment.Donor_id = donor
                appointment.save()
                messages.success(request , 'Appointment request sent successfuly')
                return redirect('/donationrequest/all')
            except:
                messages.error(request , 'Error during appointment request')
        else:
            messages.error(request , 'Error during appointment request')
    context = {'form':form , 'donor':donor}
    return  render(request , 'donor/makeappointment.html', context)

            
def GetEvent(request , type):
    donor= DonorState(request)['donor']
    events = None
    try:
        if(type=='all'):
            events = Event.objects.all()
        else:
            events = Event.objects.all()[0:5]
    except:
        events=None
    context= {'events':events , 'donor':donor}
    return render(request , 'donor/events.html' , context)
def GetCamp(request , type):
    donor= DonorState(request)['donor']
    context= {'donor':donor}
    return render(request , 'donor/camps.html' , context)














