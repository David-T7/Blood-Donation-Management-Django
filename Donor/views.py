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
from Event.models import Camp, Event
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from LabTechnician.models import DeferringList
from django.utils.dateparse import parse_date 


def Register(request):
    form1 = DonorCreationForm()   # using the donor creation form created in forms.py
    form2= AddressCreationForm()
    form3= CustomUserCreationForm()
    if request.method == 'POST':
        form1= DonorCreationForm(request.POST , request.FILES)  # getting values send from the page
        form2= AddressCreationForm(request.POST)
        form3 = CustomUserCreationForm(request.POST)
        if (form1.is_valid() and form2.is_valid() and form3.is_valid()):  # checking  values send from the page are valid  
            try:
                if(int(request.POST['Age']) >=18):
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
                else:
                    messages.error(request , 'You must be 18 or above to register')
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

def EditProfile(request):
    state = request.user
    useraccount = Account.objects.get(id=state.id)
    donor= Donor.objects.get(Account_id = useraccount.id)
    form= DonorAccountEditForm (instance=donor)
    if request.method == 'POST':
        form = DonorAccountEditForm(request.POST, request.FILES, instance=donor)
        if (form.is_valid()):
            try:
                form.save()
            except:
                messages.error(request,'Error occured during updating profile pic')
        else:
                messages.error(request,'please input correct information')
        request.user.save()
    context = {'form': form , 'donor':donor , 'sender':'profile'}
    return render(request, 'donor/editprofile.html', context)

def EditUserName(request):
    state = request.user
    donor = DonorState(request)['donor']
    form= CustomUserChangeForm (instance=state)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=state)
        if (form.is_valid()):
            try:
                form.save()
            except:
                messages.error(request,'Error occured during updating username')
        else:
                messages.error(request,'please input correct information')
        request.user.save()
    context = {'form': form , 'donor':donor , 'sender':'username'}
    return render(request, 'donor/editusername.html', context)




def EditPassword(request):
    donor = DonorState(request)['donor']
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if (form.is_valid()):
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request , 'Successfuly updated password')
            except:
                messages.error(request,'Error occured during updating password')
        else:
                messages.error(request,'please input correct information')
        request.user.save()
    context = {'form': form ,'donor':donor , 'sender':'password' }
    return render(request, 'donor/editpassword.html', context)






    
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
        elif(type=='notall'):
            donation = DonationRequestFormResult.objects.filter(Donor_id = donor.Donor_id)[0:5]
        elif(type=='searched'):
            print('in searched ')
            if request.method == 'POST':
                print('in post')
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'RequestDate'):
                    date = parse_date(searched)
                    donation = DonationRequestFormResult.objects.filter(Request_Date =  date)
                    print('donation found',donation)
                elif(searchby == 'RequestStatus'):
                    donation = DonationRequestFormResult.objects.filter(Status =  searched)
                    print('donation by reqstatus found',donation[0].Status)
                elif(searchby == 'AppointmentDate'):
                    date = parse_date(searched)
                    app = Appointment.objects.get(Date = date)
                    donation = DonationRequestFormResult.objects.filter(Donor_id = app.Donor_id)
                elif(searchby == 'AppointmentStatus'):
                    app = Appointment.objects.get(Status =  searched)
                    donation = DonationRequestFormResult.objects.filter(Donor_id = app.Donor_id)

    except:
        donation = None
    try:
        if(type=='all'):
            appointment = Appointment.objects.filter(Donor_id = str(donor.Donor_id))
        elif(type=='notall'):
            appointment = Appointment.objects.filter(Donor_id = str(donor.Donor_id))[0:5]
        elif(type=='searched'):
            if(searchby == 'AppointmentDate'):
                    date = parse_date(searched)
                    appointment = Appointment.objects.filter(Date = date)
            elif(searchby == 'AppointmentStatus'):
                    appointment = Appointment.objects.filter(status =  searched)
            elif(searchby == 'RequestDate'):
                    date = parse_date(searched)
                    dn = DonationRequestFormResult.objects.get(Request_Date =  date)
                    appointment = Appointment.objects.filter(Donor_id = str(dn.Donor_id))
                    print('appointment found',appointment[0])
            elif(searchby == 'RequestStatus'):
                    dn = DonationRequestFormResult.objects.get(Status =  searched)
                    appointment = Appointment.objects.filter(Donor_id = str(dn.Donor_id))
                    print('appointment by donation status found',appointment[0].status)

    except:
        print('no appointment')
        appointment = None
    my_list=[]
    try:
        my_list = list(itertools.zip_longest(donation,appointment))
        print('list is set')
    except:
        my_list = []
        print('list is empty')
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
        elif(type=='notall'):
            events = Event.objects.all()[0:5]
        elif(type=='searched'):
            print('in searched ')
            if request.method == 'POST':
                print('in post')
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'EventName'):
                    events = Event.objects.filter(EventName = searched)
                elif(searchby == 'EventType'):
                     events = Event.objects.filter(EventType = searched)
                elif(searchby == 'EventDate'):
                    date = parse_date(searched)
                    events = Event.objects.filter(EventDate = date)  
    except:
        events=None
    context= {'events':events , 'donor':donor}
    return render(request , 'donor/events.html' , context)




def Camps(request , type):
    donor= DonorState(request)['donor']
    camps = None
    try:
        if(type=='all'):
            camps=Camp.objects.all()
        elif(type=='notall'):
            camps=Camp.objects.all()[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                print('in post')
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'Name'):
                    camps = Camp.objects.filter(CampsName = searched)
                elif(searchby == 'City'):
                     camps = Camp.objects.filter(city = searched)
                elif(searchby == 'Kebele'):
                    camps = Camp.objects.filter(CampsKebele = searched) 
    except:
        camps=None
    context={'camps':camps , 'donor': donor}
    return render(request ,'donor/camps.html' , context)

def SeeCamp(request , pk):
    donor= DonorState(request)['donor']
    camp = None
    try:
        camp = Camp.objects.get(Camps_id=pk)
    except:
        camp = None
    context={'camp':camp , 'donor':donor}
    return render(request ,'donor/seecamp.html' , context)










