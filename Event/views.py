from django.shortcuts import redirect, render
from django.views.generic import ListView

from .models import Camp , Event
from .forms import EventCreationForm , CampCreationForm
from django.contrib import  messages
from UserAccount.models import UserRegistration
from django.utils.dateparse import parse_date 

def bbmanagerstate(request):
    bbmanager = request.user
    account = UserRegistration.objects.get(Account_id=bbmanager.id)
    context={'account':account}
    return context
def Camps(request):
    camps = Camp.objects.all()
    context={'camps':camps , 'account':bbmanagerstate(request)['account']}
    return render(request, 'bbmanager/camps.html' , context)
def Camps(request , type):
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
    context={'camps':camps , 'account':bbmanagerstate(request)['account']  , 'type':type}
    return render(request ,'bbmanager/camps.html' , context)

def SeeCamp(request , pk):
    camp = None
    try:
        camp = Camp.objects.get(Camps_id=pk)
    except:
        camp = None
    context={'camp':camp , 'account':bbmanagerstate(request)['account']}
    return render(request ,'bbmanager/seecamp.html' , context)

def Events(request , type):
    events = None
    try:
        if(type=='all'):
            events=Event.objects.all()
        elif(type=='notall'):
            events=Event.objects.all()[0:5]
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
    context={'events':events , 'account':bbmanagerstate(request)['account'] , 'type':type }
    return render(request ,'bbmanager/events.html' , context)
def CreateEvent(request):
    form = EventCreationForm()
    if request.method == 'POST':
        form= EventCreationForm(request.POST,request.FILES)
        if (form.is_valid()):
            try:
                events = form.save(commit=False)
                events.save()
                messages.success(request, 'Successfully Added event')
                return redirect('/events/notall')
            except:
                events = None   
    context = {'form': form , 'type':'add' , 'account':bbmanagerstate(request)['account']}
    return render(request, 'bbmanager/addevent.html',context)

def CreateCamp(request):
    form = CampCreationForm()
    if request.method == 'POST':
        form= CampCreationForm(request.POST,request.FILES )
        if (form.is_valid()):
            try:
                camp = form.save(commit=False)
                camp.save()
                messages.success(request, 'Successfully Added camp')
                return redirect('/camps/notall')
            except:   
                camp = None
    context = {'form': form , 'type':'add' , 'account':bbmanagerstate(request)['account']}
    return render(request, 'bbmanager/addcamp.html',context)

def UpdateCamp(request , pk ):
    camp = None
    try:
        camp = Camp.objects.get(Camps_id=pk)
        form = CampCreationForm(instance=camp)
    except:
        camp=None
        form = CampCreationForm()
    if request.method == 'POST':
        form = CampCreationForm(request.POST,request.FILES ,  instance=camp)
        if form.is_valid():
            form.save()
            messages.success(request, 'Camp was updated successfully!')
            return redirect('/camps/notall')
    context = {'form': form , 'type':'update' , 'account':bbmanagerstate(request)['account']}
    return render(request, 'bbmanager/addcamp.html', context)





def UpdateEvent(request , pk ):
    event = None
    try:
        event = Event.objects.get(Event_id=pk)
        form = EventCreationForm(instance=event)
    except:
        event =None
        form = EventCreationForm()
    if request.method == 'POST':
        form = EventCreationForm(request.POST,request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'event was updated successfully!')
            return redirect('/events/notall')
        else:
            messages.success(request, 'event was not updated successfully!')
    context = {'form': form , 'type':'update' , 'account':bbmanagerstate(request)['account']}
    return render(request, 'bbmanager/addevent.html', context)

def DeleteEvent(request , pk):
    event = None
    try:
        event = Event.objects.get(Event_id=pk)
    except:
        event= None
    try:
        event.delete()
        messages.success(request, 'event was deleted successfully!')
        return redirect('/events/notall')
    except:
        messages.success(request, 'event was not deleted successfully!')
    return render(request, 'bbmanager/events.html')
def DeleteCamp(request , pk):
    camp =None
    try:
        camp = Camp.objects.get(Camps_id=pk)
    except:
        camp =None
    try:
        camp.delete()
        messages.success(request, 'Camp was deleted successfully!')
        return redirect('/camps/notall')
    except:
        messages.success(request, 'Camp was not deleted successfully!')
    return render(request, 'bbmanager/camps.html')