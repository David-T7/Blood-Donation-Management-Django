from django.contrib import  messages
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth import login, authenticate, logout
from Hospital.models import Hospital
from Donor.models import Donor
from UserAccount.models import Account ,  UserRegistration
from UserAccount.forms import  CustomUserChangeForm, CustomUserCreationForm, ProfilePictureUpdateForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm 

class HomePage(ListView):   # class based view for just rendering the home page         
    model= Account           
    template_name = 'home.html' 

class AboutUs(ListView):       
    model= Account           
    template_name = 'aboutus.html' 


def Login(request , role):          # function based view for handling user login
    form = CustomUserCreationForm()
    if request.method == 'POST':
        username = request.POST['username'].lower()      # making sure the user name is in lowercase 
        password = request.POST['password1']
        try:
            user = authenticate(request=request, username=username, password=password)   # full user authenticaton including role
            if user is not None:
                login(request, user) 
                if(user.Role.lower() =='bbmanager' ):    
                    return redirect('/bbdashbord/notall')  # redircting to other page after login
                elif(user.Role.lower() =='donor'):
                    return redirect('/donordashbord/notall')
                elif(user.Role.lower()=='nurse'):
                    return redirect('/donorrequest/notall')
                elif(user.Role.lower()=='labtechnician'):
                    return redirect('/labdonationrequest/notall')
                elif(user.Role =='HospitalRepresentative'):
                    return redirect('/hospitaldashbord/notall')
            else:
                login(request, user , backend='django.contrib.auth.backends.ModelBackend')
        except:
            try:
                testusername = Account.objects.get(username = username)
                messages.error(request, 'Incorrect Password')
            except:
                messages.error(request, 'Username doestnot exist')
    return render(request, 'login.html',{'Role':role,'form':form})  

def Logout(request):
    logred = '/login/' + request.user.Role  # getting the redirection path for every role
    logout(request)
    messages.info(request, 'Successfuly Logged out!')    
    return redirect(logred)

def ForgotPassword(request,role):  # not implemented 
    return render(request , 'forgot.html',{'Role':role})

def ResetPassword(request,role): # not implemtented
    return render(request,'reset.html',{'Role':role})


def Userstate(request):  # for getting the state of the user 
    state = request.user
    try:
        account = UserRegistration.objects.get(Account_id=state.id) 
    except:
        print("in exception")
        try:
            account = Donor.objects.get(Account_id = state.id)
        except:
            account = Hospital.objects.get(Account_id = state)
    context={'account':account}
    return context
    

def EditUserName(request):
    state = request.user # hodling the state of the user
    account = Userstate(request)['account']
    form= CustomUserChangeForm(instance=state)  # using form created in forms.py

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=state)
        if (form.is_valid()):
            try:
                form.save()
                messages.success(request,'Account updated successfuly')
            except:
                None
        request.user.save() # saving the state of the user after it is updated 
    context = {'form': form , 'account':account , 'sender':'username' , 'active_page':'editaccount'}
    if(request.user.Role.lower() == 'bbmanager'):
        return render(request, 'bbmanager/editusername.html', context)
    elif(request.user.Role.lower() == 'nurse'):
        return render(request, 'nurse/editusername.html', context)
    elif(request.user.Role.lower() == 'labtechnician'):
        return render(request, 'labtechnician/editusername.html', context)
    elif(request.user.Role.lower() == 'donor'):
        return render(request, 'donor/editusername.html', context)
    elif(request.user.Role.lower() == 'hospitalrepresentative'):
        return render(request, 'hospitalrep/editusername.html', context)

def EditProfilePicture(request):
    account = Userstate(request)['account']
    form  = ProfilePictureUpdateForm (instance=account)
    if request.method == 'POST':
        form = ProfilePictureUpdateForm(request.POST, request.FILES, instance=account)  # recieving all files from the page including the new profile pic 
        if (form.is_valid()):
            try:
                form.save()
            except:
                messages.error(request,'Error occured during updating profile pic')
        request.user.save()
    context= {'form':form , 'account':account , 'sender':'profile' , 'active_page':'editaccount'}
    if(request.user.Role.lower() == 'bbmanager'):
        return render(request, 'bbmanager/editprofile.html', context)
    elif(request.user.Role.lower() == 'nurse'):
        return render(request, 'nurse/editprofile.html', context)
    elif(request.user.Role.lower() == 'labtechnician'):
        return render(request, 'labtechnician/editprofile.html', context)
    elif(request.user.Role.lower() == 'donor'):
           return render(request, 'donor/editprofile.html', context)
    elif(request.user.Role.lower() == 'hospitalrepresentative'):
        return render(request, 'hospitalrep/editprofile.html', context)

def EditPassword(request):
    account = Userstate(request)['account']
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
        request.user.save()
    context= {'form':form , 'account':account , 'sender':'password' , 'active_page':'editaccount'}
    if(request.user.Role.lower() == 'bbmanager'):
        return render(request, 'bbmanager/editpassword.html', context)
    elif(request.user.Role.lower() == 'nurse'):
        return render(request, 'nurse/editpassword.html', context)
    elif(request.user.Role.lower() == 'labtechnician'):
        return render(request, 'labtechnician/editpassword.html', context)
    elif(request.user.Role.lower() == 'donor'):
        return render(request, 'donor/editpassword.html', context)
    elif(request.user.Role.lower() == 'hospitalrepresentative'):
        return render(request, 'hospitalrep/editpassword.html', context)

    














































































