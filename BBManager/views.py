from django.shortcuts import render
from django.contrib import  messages
from django.shortcuts import redirect, render
from Blood.models import Blood
from Donor.models import Donor 
from UserAccount.models import UserRegistration
from Hospital.models import Hospital , BloodRequest

def Userstate(request):  # for getting the state of the user 
    state = request.user
    account = UserRegistration.objects.get(Account_id=state.id) 
    context={'account':account}
    return context
def BBmanager(request):
    context=Userstate(request)
    return render(request ,  'bbmanager/bbmanager.html' , context) # sending the state of the user for the page rendered
def BBDashbord(request , type):
    bloodcount=0  # total blood count
    bloodrequest_no = 0
    acceptedblood_request = 0
    rejectedblood_request = 0
    pendingblood_request = 0
    totalbloodcout = 0
    bloodrequest=None # for holding blood request object
    try:
        bloodrequest_no = BloodRequest.objects.all().count()
    except:
        bloodrequest_no = 0
    try:
        acceptedblood_request = len(BloodRequest.objects.filter(Status = 'accepted'))
    except:
        acceptedblood_request = 0
    try:
        rejectedblood_request = len(BloodRequest.objects.filter(Status = 'rejected'))
    except:
        rejectedblood_request = 0
    try:
        pendingblood_request = len(BloodRequest.objects.filter(Status = 'in progress'))
    except:
        pendingblood_request = 0
    try:
        if(type=='all'):
            bloodrequest = BloodRequest.objects.all()  
        else:
            bloodrequest = BloodRequest.objects.all()[0:5]
    except:
        bloodrequest= None
    try:
        for bl in Blood.objects.all():
            totalbloodcout+=int(bl.QuantityOfBlood[:-2])
    except:
        totalbloodcout=0
    context={'donors_count': Donor.objects.count() ,
                   'hospitals_count': Hospital.objects.count(),
                   'recent_blood_count':bloodcount,
                   'bloodrequest':bloodrequest,
                   'totalbloodcount':totalbloodcout,
                   'bloodrequest_no':bloodrequest_no,
                   'acceptedrequest':acceptedblood_request,
                   'rejectedrequest':rejectedblood_request,
                   'pendingrequest':pendingblood_request,
                   'hospitals':Hospital.objects.all(),
                   'account':Userstate(request)['account'],
                   'sender':'dashbord',
                   'type':type,
    }
    return render(request, 'bbmanager/dashbord.html' ,context)