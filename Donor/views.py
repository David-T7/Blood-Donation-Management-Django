from datetime import date
import itertools
from multiprocessing import context
import re
from sqlite3 import Date
from time import time
from django.contrib import  messages
from django.shortcuts import redirect, render
from Donor.forms import AppointmentCreationForm, DonationRequestQuestionForm, DonorCreationForm , DonationRequestFormQuesitons, DonorAccountEditForm , RequestAnswerCreationForm
from Donor.models import Appointment, Donor
from UserAccount.models import Account , Address
from UserAccount.forms import AddressCreationForm, CustomUserCreationForm , CustomUserChangeForm
from Donor.models import DonationRequestFormResult , DonationRequestFormQuesitons 
from Event.models import Camp, Event
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from LabTechnician.models import DeferringList
from django.utils.dateparse import parse_date , parse_time
from .forms import AppointmentCreationForm
from datetime import datetime, timedelta


def Register(request):
    form1 = DonorCreationForm()   # using the donor creation form created in forms.py
    form2= AddressCreationForm()
    form3= CustomUserCreationForm()
    
    if request.method == 'POST':
        form1= DonorCreationForm(request.POST , request.FILES)  # getting values send from the page
        form2= AddressCreationForm(request.POST)
        form3 = CustomUserCreationForm(request.POST)
        
        if (form1.is_valid() and form2.is_valid() and form3.is_valid()):  # checking  values sent from the page are valid  
            try:
                print("in try")
                dob_string = request.POST['DateOfBirth'] 
                print (dob_string)
                dob_datetime = datetime.strptime(dob_string, '%Y-%m-%d')
                print(dob_datetime)
                year_of_birth = dob_datetime.year
                print(year_of_birth)
                current_year = datetime.now().year
                
                if current_year - year_of_birth >= 18:
                    account = form3.save(commit=False) # saving the values but not in the table
                    account.Role='Donor'
                    account.email = request.POST['Email']
                    account.save() # saving the user account
                    address = form2.save(commit=False)
                    try:
                        address.save()
                    except:
                        messages.error(request, 'Please fill the address form completely')
                        del account    
                    try:
                        donor = form1.save(commit=False)
                        phone = request.POST['Phone']
                        donor.Address_id= Address.objects.get(Phone=phone)  # assigning donor_id field in donor form address table using phone
                        donor.Account_id = account
                        donor.save()
                        messages.success(request, 'Successfully Registered')
                        print("successfully registered")
                        return redirect('login/Donor')
                        
                    except:
                        messages.error(request, 'Please fill the donor form completely')
                        del account
                else:
                    messages.error(request , 'You must be 18 or above to register')
                    print("age is less than 18")
            except:
                True
        else:
            print("form is not valid")
    context = {'form1': form1,'form2':form2,'form3':form3 , 'sender':'donor'}  # forms that are passed to the page rendered
    return render(request, 'registerpage.html', context)


def DonorState(request):
    donor = request.user
    context = {'donor': Donor.objects.get(Account_id = donor.id) }
    return context

def Donors(request):
    context = {'user':request.user , 'donor':DonorState(request)['donor']}
    return render(request , 'donor/donor.html' , context)

# def EditProfile(request):
#     state = request.user
#     useraccount = Account.objects.get(id=state.id)
#     donor= Donor.objects.get(Account_id = useraccount.id)
#     form= DonorAccountEditForm (instance=donor)
#     if request.method == 'POST':
#         form = DonorAccountEditForm(request.POST, request.FILES, instance=donor)
#         if (form.is_valid()):
#             try:
#                 form.save()
#             except:
#                 messages.error(request,'Error occured during updating profile pic')
#         request.user.save()
#     context = {'form': form , 'donor':donor , 'sender':'profile' , 'active_page':'editaccount'}
#     return render(request, 'donor/editprofile.html', context)

# def EditUserName(request):
#     state = request.user
#     donor = DonorState(request)['donor']
#     form= CustomUserChangeForm (instance=state)
#     if request.method == 'POST':
#         form = CustomUserChangeForm(request.POST, instance=state)
#         if (form.is_valid()):
#             try:
#                 form.save()
#             except:
#                 messages.error(request,'Error occured during updating username')
#         request.user.save()
#     context = {'form': form , 'donor':donor , 'sender':'username' , 'active_page':'editaccount'}
#     return render(request, 'donor/editusername.html', context)




# def EditPassword(request):
#     donor = DonorState(request)['donor']
#     form = PasswordChangeForm(request.user)
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)

#         if (form.is_valid()):
#             try:
#                 user = form.save()
#                 update_session_auth_hash(request, user)
#                 messages.success(request , 'Successfuly updated password')
#             except:
#                 messages.error(request,'Error occured during updating password')
#         request.user.save()
#     context = {'form': form ,'donor':donor , 'sender':'password' , 'active_page':'editaccount' }
#     return render(request, 'donor/editpassword.html', context)






    
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
            'type':type,
            'sender':'dashbord',
            'active_page':'home'
    }
    return render(request, 'donor/dashbord.html' ,context)

def DonationRequest(request , type):
    print('in donor request')
    donor = DonorState(request)['donor']
    donation = None
    appointment = None
    try:
        if(type=='all'):
            donation = DonationRequestFormResult.objects.filter(Donor_id = donor.Donor_id)
        elif(type=='notall'):
            donation = DonationRequestFormResult.objects.filter(Donor_id = donor.Donor_id)[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'RequestDate'):
                    date = parse_date(searched)
                    donation = DonationRequestFormResult.objects.filter(Request_Date =  date)
                elif(searchby == 'RequestStatus'):
                    donation = DonationRequestFormResult.objects.filter(Donor_id = donor.Donor_id , Status =  searched)
                elif(searchby == 'AppointmentDate'):
                    date = parse_date(searched)
                    app = Appointment.objects.filter(Date = date)
                    donation = DonationRequestFormResult.objects.filter(Donor_id = app[0].Donor_id)
                elif(searchby == 'AppointmentStatus'):
                    app = Appointment.objects.filter(status =  searched)
                    donation = DonationRequestFormResult.objects.filter(Donor_id = str(app[0].Donor_id))

    except:
        donation = None
    try:
        if(type=='all'):
            appointment = Appointment.objects.filter(Donor_id = str(donor.Donor_id))
        elif(type=='notall'):
            appointment = Appointment.objects.filter(Donor_id = str(donor.Donor_id))[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                searchby = request.POST['searchby']
                searched = request.POST['searched']
            if(searchby == 'AppointmentDate'):
                    date = parse_date(searched)
                    appointment = Appointment.objects.filter(Date = date)
            elif(searchby == 'AppointmentStatus'):
                    appointment = Appointment.objects.filter(status =  searched)
            elif(searchby == 'RequestDate'):
                    appointment = Appointment.objects.filter(Donor_id = donation[0].Donor_id)
            elif(searchby == 'RequestStatus'):
                    appointment = Appointment.objects.filter(Donor_id = donation[0].Donor_id)
    except:
        appointment = None
    my_list=[]
    try:
        my_list = list(itertools.zip_longest(donation,appointment))
        print('list found ')
    except:
        my_list = []
        print('list not set')
    context = {'list':my_list , 'donation':donation ,'type':type, 'donor':donor , 'searchtype':type , 'active_page':'donationrequest'}
    return render (request , 'donor/donationrequest.html' , context  )

def MakeDonationRequest(request):
    donor = DonorState(request)['donor']
    form = RequestAnswerCreationForm()
    todays_req = 0
    request_limit_daily = 3
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
    try:
        today = date.today()
        todays_req = len(DonationRequestFormResult.objects.filter(Request_Date = today , Donor_id = donor  ))
    except:
        todays_req = 0
    if (not deferringList and todays_req <= request_limit_daily):
        if request.method == 'POST':
            form= RequestAnswerCreationForm(request.POST)
            if (form.is_valid()):
                try:
                    req = form.save(commit=False)
                    req.Donor_id = donor   
                    req.save()
                    messages.success(request , 'request sent successfuly')
                    return redirect('/donationrequest/notall')
                except:
                    messages.success(request , 'error during request')
            else:
                messages.success(request , 'request was not successful')
    else:
        if(deferringList):
            messages.error(request , 'Sorry you cant make a donation because of health issues')
            return redirect('/donationrequest/notall')
        elif(todays_req > request_limit_daily):
            messages.error(request , 'You have reached request limit for today')
            return redirect('/donationrequest/notall')
    context = { 'form':form , 'questions':questions , 'donor':donor , 'type':'add' ,  'active_page':'donationrequest'}
    return render(request, 'donor/createdonationrequest.html',context)    


def CancelRequest(request , pk):
    donor = DonorState(request)['donor']
    donreq = None
    context = { 'active_page':'donationrequest'}
    try:
        donreq = DonationRequestFormResult.objects.get(Result_id = pk)
        donreq.delete()
        messages.success(request , 'You have successfuly canceled the request')
        return redirect('/donationrequest/notall' , context)

    except:
        messages.success(request , 'Error during canceling the request')
        return redirect('/donationrequest/notall' , context)


def UpdateRequest(request , pk):
    donor = DonorState(request)['donor']
    questions = None
    donreq = None
    try:
        donreq = DonationRequestFormResult.objects.get(Result_id=pk)
    except:
        donreq = None
    try:
        questions = DonationRequestFormQuesitons.objects.all()[0]
    except:
        questions = None
    form = RequestAnswerCreationForm(instance= donreq)
    if request.method == 'POST':
        form = RequestAnswerCreationForm(request.POST, instance=donreq)
        if form.is_valid():
            form.save()
            messages.success(request, 'Request was updated successfully!')
            return redirect('/donationrequest/notall') 
        else:
            messages.success(request, 'event was not updated successfully!')
    context = { 'form':form  , 'donor':donor , 'questions':questions ,  'type':'update' ,  'active_page':'donationrequest'}
    return render(request, 'donor/createdonationrequest.html', context)    





# def AppointmentChoices(request , type , sender , pk):
#     donor = DonorState(request)['donor']
#     choices = None
#     try:
#         if(type == 'all'):
#             choices = AppointmentChoice.objects.all()
#         elif (type == 'notall'):
#             choices = AppointmentChoice.objects.all()[0:5]
#         elif(type=='searched'):
#             if request.method == 'POST':
#                 searchby = request.POST['searchby']
#                 searched = request.POST['searched']
#             if(searchby == 'AppointmentDate'):
#                     date = parse_date(searched)
#                     choices = AppointmentChoice.objects.filter(Date = date)
#             elif(searchby == 'AppointmentTime'):
#                     time = parse_time(searched)
#                     choices = AppointmentChoice.objects.filter(Time = time)    
#     except:
#         choices = None
#     context = {'donor':donor, 'choices':choices , 'type':type , 'sender':sender , 'pk':pk  }
#     return render (request , 'donor/chooseappointment.html' ,  context)




def MakeAppointment(request ):
    donor = DonorState(request)['donor']
    form = AppointmentCreationForm()
    if request.method == 'POST':
        form= AppointmentCreationForm(request.POST)
        if (form.is_valid()):
            try:
                app = form.save(commit=False)
                app.Donor_id = donor
                app.save()
                return redirect('/getappointments/notall')
            except:
                messages.error(request , 'Error during appointment request')
    context = {'donor':donor ,'type':'add', 'form':form , 'active_page':'appointment'}
    return  render(request , 'donor/chooseappointment.html', context)

def UpdateAppointment(request , pk):
    donor = DonorState(request)['donor']
    app=None
    try:
        app = Appointment.objects.get(App_id = pk)
        form = AppointmentCreationForm(instance=app)
    except:
        app=None
        form = AppointmentCreationForm(instance=app)
    if request.method == 'POST':
        form = AppointmentCreationForm(request.POST,  instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment was updated successfully!')
            return redirect('/getappointments/notall')
        else:
            messages.success(request, 'Appointment was not updated successfully!')
    context = {'form': form , 'type':'update' , 'donor':donor , 'active_page':'appointment'}
    return render(request, 'donor/chooseappointment.html', context)

            

def CancelAppointment(request , pk):
    donor = DonorState(request)['donor']
    app = None
    context = {'active_page':'appointment'}
    try:
        app = Appointment.objects.get(App_id = pk)
        app.delete()
        messages.success(request , 'Appointment Canceled successfuly' , context)
        return redirect('/getappointments/notall')
    except:
        messages.error(request , 'Error during canceling appointment' , context)
        return redirect('/getappointments/notall')

def GetAppointments(request , type):
    donor = DonorState(request)['donor']
    appointment = None
    try:
        if(type=='all'):
            appointment = Appointment.objects.all()
        elif(type == 'notall'):
            appointment = Appointment.objects.all()[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'Date'):
                    date = parse_date(searched)
                    appointment = Appointment.objects.filter(Date =  date)
                elif(searchby == 'Status'):
                    appointment = Appointment.objects.filter(status =  searched.lower())
    except:
        appointment = None
    context= {'appointments':appointment , 'donor':donor ,  'active_page':'appointment'}
    return render(request , 'donor/appointment.html' , context)

    


            
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
    context= {'events':events , 'donor':donor , 'type':type , 'active_page':'event'}
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
    context={'camps':camps , 'donor': donor , 'type':type , 'active_page':'camp'}
    return render(request ,'donor/camps.html' , context)

def SeeCamp(request , pk):
    donor= DonorState(request)['donor']
    camp = None
    try:
        camp = Camp.objects.get(Camps_id=pk)
    except:
        camp = None
    context={'camp':camp , 'donor':donor , 'active_page':'camp'}
    return render(request ,'donor/seecamp.html' , context)










