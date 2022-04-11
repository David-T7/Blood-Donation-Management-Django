from django.shortcuts import render
from multiprocessing import context
from django.contrib import  messages
from django.shortcuts import redirect, render
from Donor.forms import DonationRequestQuestionForm, DonationRequestFormQuesitons
from Donor.models import  Appointment
from UserAccount.models import  Address, UserRegistration
from Donor.models import DonationRequestFormResult , DonationRequestFormQuesitons , Appointment , Donor

def Userstate(request):  # for getting the state of the user 
    state = request.user
    account = UserRegistration.objects.get(Account_id=state.id) 
    context={'account':account}
    return context
    
def Nurse(request):
    context=Userstate(request)
    return render(request ,  'nurse/nurse.html' , context) # sending the state of the user for the page rendered

def DonationRequest(request , type):
    donreq= None
    donor_account=None
    try:
        if(type=='all'):
            donreq = DonationRequestFormResult.objects.all()
        else:
            donreq = DonationRequestFormResult.objects.all()[0:5]
    except:
        donreq = None
    try:
        donor =Donor.objects.filter(Donor_id = donreq.Donor_id)
        donor_account = Address.objects.filter(Address_id =donor.Address_id)
    except:
        donor_account=None
    context = {'account':Userstate(request)['account'] ,'donor_account':donor_account, 'donationrequest': donreq}
    return render (request , 'nurse/donationrequest.html' , context)

def CheckRequest(request , pk):
    questions = None 
    answer = None
    try:
        questions = DonationRequestFormQuesitons.objects.all()[0]
    except:
        questions = None
    try:
        answer = DonationRequestFormResult.objects.get(Result_id = pk)
    except:
        answer = None
    context = {'account':Userstate(request)['account'] , 'questions':questions , 'answers':answer}
    return render(request , 'nurse/checkrequest.html',context)

def CheckAppointments(request , type):
    appointment = None
    try:
        if(type=='all'):
            appointment = Appointment.objects.all()
        else:
            appointment = Appointment.objects.all()[0:5]
    except:
        appointment = None
    context = {'account': Userstate(request)['account'] , 'appointments':appointment}
    return render (request , 'nurse/appointment.html' , context)

def Confirmrequest(request ,  pk , type):
    try:
        req = DonationRequestFormResult.objects.get(Result_id = pk)
        if(type=='accept'):
            req.Status = 'accepted'
            req.save()
            messages.success(request,'Request was Accepted Succesfuly')
        else:
            req.Status = 'rejected'
            req.save()
            messages.success(request,'Request was Rejected Succesfuly')
        return redirect('/donorrequest/all')
    except:
        messages.error(request,'Error occured during confirmation')
    context = {'account': Userstate(request)['account']}
    return render(request , 'nurse/checkrequest.html' , context)

def confirmappointment(request , pk , type):
     try:
        app = Appointment.objects.get(App_id = pk)
        if(type=='accept'):
            app.status = 'accepted'
            app.save()
            messages.success(request,'Appointment was Accepted Succesfuly')
        else:
            app.status = 'rejected'
            app.save()
            messages.success(request,'Appointment was Rejected Succesfuly')
        return redirect('/checkappointment/all')
     except:
            messages.error(request,'Error occured during confirmation')
     context = {'account': Userstate(request)['account']}
     return render(request , 'nurse/appointment.html' , context)
        



def GetDonorAddress(request , pk):
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
    for ad in Address.objects.all():
        print(ad.Address_id)
    context = {'account': Userstate(request)['account'] , 'address':address , 'donor':acc }
    return render(request , 'nurse/checkdonoraddress.html' , context)

def DonorQuestions(request , type):
    questions = None
    try:
        if(type == 'all'):
            questions = DonationRequestFormQuesitons.objects.all()
        else:
            questions = DonationRequestFormQuesitons.objects.all()[0:3]
    except:
        question = None
    context = {'account':Userstate(request)['account'] , 'questions':questions }
    return render (request , 'nurse/donorquestions.html' , context)

def AddQuestions(request , type):
    form = DonationRequestQuestionForm()
    if request.method == 'POST':
        form = DonationRequestQuestionForm(request.POST)
        if (form.is_valid()):
            try:
                form.save()
                messages.success(request, 'Successfully Added Question')
            except:
                messages.error(request, 'Error during adding question')
        else:
            messages.error(request, 'Error during adding question')
    context = {'account':Userstate(request)['account'] , 'form':form , 'type':type}
    return render(request , 'nurse/addquestions.html' , context)

def UpdateQuestion(request , pk ):
    questions = DonationRequestFormQuesitons.objects.get(Question_id=pk)
    form = DonationRequestQuestionForm(instance=questions)
    if request.method == 'POST':
        form = DonationRequestQuestionForm(request.POST, instance=questions)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question was updated successfully!')
            return redirect('/donorquestions/notall')
        else:
            messages.success(request, 'Question was not updated successfully!')

    context = {'form': form , 'type':'update' , 'account':Userstate(request)['account']}
    return render(request, 'nurse/addquestions.html', context)

def DeleteQuestion(request , pk):
    question = DonationRequestFormQuesitons.objects.get(Question_id=pk)
    try:
        question.delete()
        messages.success(request, 'question was deleted successfully!')
        return redirect('/donorquestions/notall')
    except:
        messages.success(request, 'question was not deleted successfully!')
    return render(request, 'nurse/donorquestions.html' , context)


