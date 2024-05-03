from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib import  messages
from Donor.models import Donor
from Hospital.forms import BloodRequestForm, HospitalCreationForm, hopsitalProfilePictureForm 
from UserAccount.forms import AddressCreationForm, CustomUserChangeForm, CustomUserCreationForm
from .models import BloodRequest , Hospital, HospitalSentBloods
from Blood.models import Blood, BloodHistory
from UserAccount.models import Account, Address, UserRegistration
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.auth import update_session_auth_hash
from django.utils.dateparse import parse_date 
from datetime import date



def bbmanagerstate(request):
    bbmanager = request.user
    account = UserRegistration.objects.get(Account_id=bbmanager.id)
    context={'account':account}
    return context

def HospitalState(request):
    context = {'hospital': Hospital.objects.get( Account_id = request.user )  }
    return context

def HospitalRequest(request, type):
    bloodrequest =None
    hospitals = None
    try:
        if(type=='all'):
            bloodrequest = BloodRequest.objects.all()
        elif(type=='notall'):
            bloodrequest = BloodRequest.objects.all()[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'HospitalName'):
                    hs = Hospital.objects.get(HospitalName = searched)
                    bloodrequest = BloodRequest.objects.filter(Hospital_id = hs.Hospital_id)
                elif(searchby == 'Phone'):
                    addr = Address.objects.get(Phone = int(searched))
                    hs = Hospital.objects.get(Address_id = addr)
                    bloodrequest = BloodRequest.objects.filter(Hospital_id = hs.Hospital_id)
                elif(searchby == 'RequestDate'):
                    date = parse_date(searched)
                    bloodrequest = BloodRequest.objects.filter(Request_Date =  date)
                elif(searchby == 'RequestStatus'):
                    bloodrequest = BloodRequest.objects.filter(Status =  searched.lower())    
    except:
        bloodrequest= None
    try:
        hospitals = Hospital.objects.all()
    except:
        hospitals = None
    context={
                   'bloodrequest':bloodrequest,
                   'hospitals':hospitals,
                   'account':bbmanagerstate(request)['account'],
                   'type':type,
                   'active_page':'hospitalrequest'
    }
    return render (request , 'bbmanager/hospitalrequest.html' , context)

def  HospitalRep(request):
    hospital = HospitalState(request)['hospital']
    context = {'hospital':hospital}
    return render (request , 'hospitalrep/hospitalrep.html' , context)

def Hospitals(request , type):
    hospitals = None
    try:
        if(type=='all'):
            hospitals = Hospital.objects.all()
        elif(type=='notall'):
            hospitals = Hospital.objects.all()[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'HospitalName'):
                    hospitals = Hospital.objects.filter(HospitalName = searched)
                elif(searchby == 'Phone'):
                    addr = Address.objects.get(Phone = int(searched))
                    hospitals = Hospital.objects.filter(Address_id = addr)
                elif(searchby == 'Representative'):
                    hospitals = Hospital.objects.filter(HospitalRepresentative = searched)
    except:
        hospitals= None
    context={'hospitals' : hospitals , 'account':bbmanagerstate(request)['account'] , 'type':type , 'active_page':'hospitals'}
    return render(request ,  'bbmanager/hospitals.html' , context)
# def AddHospital(request):
#     form1 = HospitalCreationForm()
#     form2 = AddressCreationForm()
#     form3 = CustomUserCreationForm()
#     if request.method == 'POST':
#         form1= HospitalCreationForm(request.POST , request.FILES)
#         form2 = AddressCreationForm(request.POST)
#         form3 =  CustomUserCreationForm(request.POST)
#         if (form1.is_valid() and form2.is_valid() and form3.is_valid()):
#             try:
#                 account = form3.save(commit=False) # saving the values but not in the table
#                 account.Role='Donor'
#                 account.email = request.POST['Email']
#                 account.save() # saving the user account
#                 address = form2.save(commit=False)
#                 address.save()
#                 hospital = form1.save(commit=False)
#                 hospital.Address_id = address
#                 if Account.objects.get(username = hospital.Username):
#                     hospital.save()
#                 messages.success(request, 'Successfully Added Hospital')
#                 return redirect('/hospitals/notall')
#             except:
#                  try:
#                     Account.objects.get(username = hospital.Username)
#                     messages.error('unable to create hosptial')
#                  except:
#                     messages.success(request, 'Username doest not exist')
#         else:
#             messages.error(request, 'Unable to create Hospital')
#     context = {'form1': form1 ,'form2':form2 ,'type':'add' ,'sender':'bbmanager', 'account':bbmanagerstate(request)['account'] , 'active_page':'hospitals'}
#     return render(request, 'bbmanager/addhospital.html',context)


def UpdateHospital(request , pk ):
    hospital = Hospital.objects.get(Hospital_id=pk)
    address = Address.objects.get(Address_id = str(hospital.Address_id))
    form1 = HospitalCreationForm(instance=hospital )
    form2 = AddressCreationForm(instance=address )
    if request.method == 'POST':
        form1 = HospitalCreationForm(request.POST, request.FILES ,   instance=hospital)
        form2 = AddressCreationForm(request.POST , instance=address )
        if (form1.is_valid() and form2.is_valid()):
            hospital = form1.save(commit=False)
            form2.save()
            try:
                if(Account.objects.get(username = hospital.Username)):
                    hospital.save()
                    messages.success(request, 'Hospital was updated successfully!')
                    return redirect('/hospitals/notall')
            except:
                hospital = None   
    context = {'form1': form1 ,'form2':form2 , 'type':'update' , 'account':bbmanagerstate(request)['account'],'hospital':hospital , 'active_page':'hospitals'}
    return render(request, 'bbmanager/addhospital.html', context)

def DeleteHospital(request , pk):
    try:
        hospital = Hospital.objects.get(Hospital_id=pk)
        address = Address.objects.get(Address_id = str(hospital.Address_id))
        address.delete() 
        account = Account.objects.get(username = hospital.Username)
        account.delete()       
        hospital.delete()
        messages.success(request, 'Hospital was deleted successfully')
        return redirect('/hospitals/notall')    
    except:
        messages.error(request, 'Hospital was not deleted successfully!')
        return redirect('/hospitals/notall')


def BloodRequests(request , type):
    hospital = HospitalState(request)['hospital']
    bloodreq = None
    try:
        if(type=='all'):
            bloodreq = BloodRequest.objects.filter( Hospital_id  =  hospital.Hospital_id)
        elif(type=='notall'):
            bloodreq = BloodRequest.objects.filter( Hospital_id  =  hospital.Hospital_id)[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                print('in post')
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'Status'):
                    bloodreq = BloodRequest.objects.filter(Status = searched)
                elif(searchby == 'RequestDate'):
                    date = parse_date(searched)
                    bloodreq = BloodRequest.objects.filter(Request_Date =   date)  
    except:
        bloodreq = None
    context = {'bloodreq': bloodreq , 'hospital': hospital , 'type':type , 'active_page':'request'}
    return render (request , 'hospitalrep/bloodreq.html' ,   context )

def HospitalDashbord(request , type):
    hospital = HospitalState(request)['hospital']
    print('hospital id is ',hospital)
    bloodrequest_no = 0
    accepted_no = 0
    pending_no = 0
    rejected_no = 0
    bloodreq = None
    try:
        if(type=='all'):
            bloodreq = BloodRequest.objects.filter( Hospital_id = hospital.Hospital_id)
        else:
            bloodreq = BloodRequest.objects.filter( Hospital_id = hospital.Hospital_id)[0:5]
    except:
        bloodreq = None
    try:
        bloodrequest_no = len(BloodRequest.objects.filter(Hospital_id =  hospital.Hospital_id ))
    except:
        bloodrequest_no=0
    try:
        accepted_no = len( BloodRequest.objects.filter(Status = 'accepted').filter(Hospital_id = hospital.Hospital_id))
    except:
        accepted_no = 0
    try:
        pending_no = len( BloodRequest.objects.filter(Status = 'in progress').filter(Hospital_id = hospital.Hospital_id))
    except:
        pending_no = 0
    try:
        rejected_no = len( BloodRequest.objects.filter(Status = 'rejected').filter(Hospital_id = hospital.Hosital_id))
    except:
        rejected_no = 0
    context={'bloodrequest_no': bloodrequest_no ,
            'accepted_no': accepted_no,
            'pending_no':pending_no,
            'rejected_no':rejected_no ,
            'bloodreq':bloodreq,
            'hospital': hospital,
            'sender' : 'dashbord',
            'type': type , 
            'active_page':'home',
    }
    return render(request, 'hospitalrep/homepage.html' ,context)



def MakeBloodRequest(request):
    hospital = HospitalState(request)['hospital']
    form = BloodRequestForm()
    todays_req = 0
    request_limit_daily = 4
    try:
        today = date.today()
        todays_req = len(BloodRequest.objects.filter(Request_Date = today  , Hospital_id = hospital))
    except:
        todays_req = 0
        print('not found')
    if(todays_req <=  request_limit_daily):
        if request.method == 'POST':
            form= BloodRequestForm(request.POST)
            if (form.is_valid()):
                try:
                    print("in try")
                    bloodreq = form.save(commit=False)
                    blood = None
                    blood = Blood.objects.filter(BloodGroup = bloodreq.Blood_Group)
                    blood_quantity = 0
                    for blood_obj in blood:
                        blood_quantity += int(blood_obj.QuantityOfBlood)          
                    if (blood_quantity < int(bloodreq.Quantity)):
                        messagetext= 'Not enough blood on stock , there is only ' + str(blood_quantity)  + ' ML'
                        messages.error(request , messagetext )
                        
                    else:
                        bloodreq.Blood_id = blood[0]
                        bloodreq.Hospital_id = hospital
                        bloodreq.save()
                        messages.success(request , 'Request was Successful')
                        return redirect('/bloodrequest/notall')
                except:
                    blood =None
                    try:
                        blood = Blood.objects.filter(BloodGroup = request.POST['Blood_Group'])
                    except:
                        blood =None
                    if(blood):
                        volumes =''
                        for bl in blood:
                            volumes+= bl.QuantityOfBlood
                        messages.error(request ,'Bloods in the stock with that group is ' + volumes + " ML"  )
                    else:
                        messages.error(request , 'Not enough blood on stock')
            else:
                messages.success(request , 'request was not successful')
    else:
        messages.error(request , 'You have reached the request limit for today')
        return redirect('/bloodrequest/notall')

    context = {'form':form ,  'hospital': hospital , 'active_page':'request'}
    return render(request, 'hospitalrep/makebloodrequest.html',context)   


def EditHospitalProfilePicture(request):
    hospital = HospitalState(request)['hospital']
    form = hopsitalProfilePictureForm(instance= hospital)
    if request.method == 'POST':
        form = hopsitalProfilePictureForm (request.POST, request.FILES ,  instance=hospital)
        if(form.is_valid()):
            try:
                form.save()
                messages.success(request,'Account updated successfuly')
            except:
                messages.success(request,'Account updated was not successful')
        else:
                messages.error(request,'Error during updating account ')
    context = {'form':form , 'hospital':hospital  }
    return render (request , 'hospitalrep/editprofilepic.html' , context)

def EditUserName(request):
    state = request.user
    hospital = HospitalState(request)['hospital']
    form= CustomUserChangeForm (instance=state)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=state)
        if (form.is_valid()):
            try:
                form.save()
                messages.success(request , 'Sucessfuly updated user name')
            except:
                messages.error(request,'Error occured during updating username')
        else:
                messages.error(request,'please input correct information')
        request.user.save()
        try:
            hospital.Username = request.user.username
            hospital.save()
        except:
            messages.error(request,'Error during updating username')

    context = {'form': form , 'hospital':hospital , 'sender':'username'}
    return render(request, 'hospitalrep/editusername.html', context)


def EditHospitalAccount(request):
    hospital = HospitalState(request)['hospital']
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if (form.is_valid()):
            try:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.error(request,'Password Was  Updated Successfuly')

            except:
                messages.error(request,'Error occured during updating password')
        else:
                messages.error(request,'please input correct information')
         # saving the state of the user after it is updated
        request.user.save()
    context= {'form':form , 'hospital':hospital}
    return render(request , 'hospitalrep/editaccount.html' , context)

def GetHopsitalAddress(request , pk):
    print('hos id is',str(pk))
    account = bbmanagerstate(request)['account']
    address = None
    acc = None
    try:
            acc = Hospital.objects.get(HospitalName = str(pk))
    except:
            acc = None
    try:
        address = Address.objects.get(Address_id = str(acc.Address_id))
    except:
        address= None
    context = {'account':account ,'address':address , 'hospital':acc , 'active_page':'hospitals' }
    return render(request , 'bbmanager/hospitaladdress.html' , context)
            
def AcceptBloodRequest(request , pk ,  type):
    account = bbmanagerstate(request)['account']
    try:
        if(type=='accept'):
            breq = BloodRequest.objects.get(Blood_Req_Id = pk)
            breq.Status = 'accepted'
            breq.save()
            blood= Blood.objects.get(Blood_id = str(breq.Blood_id.Blood_id))
            BloodHistory.objects.create(Blood_id=blood.Blood_id , Donor_id = blood.Donor_id.Donor_id ,BloodGroup = blood.BloodGroup , 
            PackNo = blood.PackNo , RegDate = blood.RegDate , ExpDate = blood.ExpDate , QuantityOfBlood = breq.Quantity , Action='Removed')
            HospitalSentBloods.objects.create(Blood_Req_Id = breq.Blood_Req_Id , Blood_id=blood.Blood_id)
            if (breq.Quantity == blood.QuantityOfBlood):
                blood.delete()
            else:
                blood.QuantityOfBlood = str(int(blood.QuantityOfBlood) - int(breq.Quantity))
                blood.save()

            messages.success(request,'Request was Accepted Succesfuly')
        elif(type=='firstreject'):
            breq = BloodRequest.objects.get(Blood_Req_Id = pk)
            breq.Status = 'rejected'
            breq.save()
            messages.success(request,'Request was Rejected Successfully')
        elif(type=='secondreject'):
            breq = BloodRequest.objects.get(Blood_Req_Id = pk)
            breq.Status = 'rejected'
            breq.save()
            sentblood = HospitalSentBloods.objects.get(Blood_Req_Id = breq.Blood_Req_Id)
            removedblood = BloodHistory.objects.filter(Blood_id = sentblood.Blood_id)[0]
            donor = Donor.objects.get(Donor_id = removedblood.Donor_id)
            blood = Blood.objects.create(Donor_id = donor , BloodGroup = removedblood.BloodGroup ,  
            PackNo = removedblood.PackNo , RegDate= removedblood.RegDate ,ExpDate = removedblood.ExpDate ,QuantityOfBlood= removedblood.QuantityOfBlood)
            BloodHistory.objects.create(Blood_id=blood.Blood_id , Donor_id = blood.Donor_id.Donor_id ,BloodGroup = blood.BloodGroup , 
                PackNo = blood.PackNo , RegDate = blood.RegDate , ExpDate = blood.ExpDate , QuantityOfBlood = blood.QuantityOfBlood , Action='Added')
            breq.Blood_id = blood
            breq.save()
            sentblood.delete()
            messages.success(request,'Request was Rejected Successfully')
        return redirect('/hospitalrequest/notall')
    except:
        breq = BloodRequest.objects.get(Blood_Req_Id = pk)
        breq.Status = 'in progress'
        breq.save()
        messages.error(request,'Error During confirming Request')
        return redirect('/hospitalrequest/notall')
    context = {'account':account}
    return render (request , 'bbmanager/hospitalrequest.html', context)
    


















