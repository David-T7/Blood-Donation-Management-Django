from django.shortcuts import redirect, render
from django.views.generic import ListView

from .models import Camp , Event
from .forms import EventCreationForm , CampCreationForm
from django.contrib import  messages
from UserAccount.models import UserRegistration

def bbmanagerstate(request):
    bbmanager = request.user
    account = UserRegistration.objects.get(Account_id=bbmanager.id)
    context={'account':account}
    return context
def Camps(request):
    camps = Camp.objects.all()
    context={'camps':camps , 'account':bbmanagerstate(request)['account']}
    return render(request, 'bbmanager/camps.html' , context)
def Events(request , type):
    events = None
    try:
        if(type=='all'):
            events=Event.objects.all()
        else:
            events=Event.objects.all()[0:5]
    except:
        events=None
    context={'events':events , 'account':bbmanagerstate(request)['account']}
    return render(request ,'bbmanager/events.html' , context)
def CreateEvent(request):
    form = EventCreationForm()
    if request.method == 'POST':
        form= EventCreationForm(request.POST)
        if (form.is_valid()):
            try:
                events = form.save(commit=False)
                events.save()
                messages.success(request, 'Successfully Added event')
                return redirect('/events/notall')
            except:   
                messages.error(request, 'An error has occurred during adding event')
        else:
            messages.error(
                request, 'An error has occurred during adding event')
    context = {'form': form , 'type':'add' , 'account':bbmanagerstate(request)['account']}
    return render(request, 'bbmanager/addevent.html',context)

def UpdateEvent(request , pk ):
    event = Event.objects.get(Event_id=pk)
    form = EventCreationForm(instance=event)
    if request.method == 'POST':
        form = EventCreationForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'event was updated successfully!')
            return redirect('/events/notall')
        else:
            messages.success(request, 'event was not updated successfully!')

    context = {'form': form , 'type':'update' , 'account':bbmanagerstate(request)['account']}
    return render(request, 'bbmanager/addevent.html', context)

def DeleteEvent(request , pk):
    event = Event.objects.get(Event_id=pk)
    try:
        event.delete()
        messages.success(request, 'event was deleted successfully!')
        return redirect('/events/notall')
    except:
        messages.success(request, 'event was not deleted successfully!')
    return render(request, 'bbmanager/events.html')

def CreateCamp(request):
    form = CampCreationForm()
    if request.method == 'POST':
        form= CampCreationForm(request.POST)
        if (form.is_valid()):
            try:
                camp = form.save(commit=False)
                camp.save()
                messages.success(request, 'Successfully Added Camp')
            except:   
                messages.error(request, 'An error has occurred during adding camp')
        else:
            messages.error(
                request, 'An error has occurred during adding camp')
    context = {'form': form , 'account':bbmanagerstate(request)['account']}
    return render(request, 'bbmanager/addcamp.html',context)