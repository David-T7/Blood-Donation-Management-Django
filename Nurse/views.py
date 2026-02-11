from django.shortcuts import render
from multiprocessing import context
from django.contrib import  messages
from django.shortcuts import redirect, render
from Donor.forms import DonationRequestQuestionForm
from Donor.models import  Appointment, DonationRequestQuestion

from UserAccount.models import  Address, UserRegistration
from Donor.models import DonationRequestFormResult , DonationRequestFormQuesitons , Appointment , Donor
from django.utils.dateparse import parse_date  , parse_time
import uuid

def Userstate(request):  # for getting the state of the user
    state = request.user
    try:
        account = UserRegistration.objects.get(Account_id=state.id)
        context={'account':account}
    except UserRegistration.DoesNotExist:
        # If user doesn't have a UserRegistration entry, return user object instead
        context={'account':state}
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
        elif(type=='notall'):
            donreq = DonationRequestFormResult.objects.all()[0:5]
        elif(type=='searched'):
            if request.method == 'POST':
                searchby = request.POST['searchby']
                searched = request.POST['searched']
                if(searchby == 'DonorName'):
                    dn = Donor.objects.filter(Donorname = searched)
                    donreq = DonationRequestFormResult.objects.filter(Donor_id = dn[0].Donor_id)
                elif(searchby == 'Phone'):
                    addr = Address.objects.get(Phone = int(searched))
                    dn = Donor.objects.get(Address_id = addr)
                    donreq = DonationRequestFormResult.objects.filter(Donor_id = dn.Donor_id)
                elif(searchby == 'RequestDate'):
                    date = parse_date(searched)
                    donreq = DonationRequestFormResult.objects.filter(Request_Date =  date)
                elif(searchby == 'RequestStatus'):
                    donreq = DonationRequestFormResult.objects.filter(Status =  searched.lower())
               
    except:
        donreq = None
    try:
        donor =Donor.objects.filter(Donor_id = donreq.Donor_id)
        donor_account = Address.objects.filter(Address_id =donor.Address_id)
    except:
        donor_account=None
    context = {'account':Userstate(request)['account'] ,'donor_account':donor_account,'type':type ,'donationrequest': donreq , 'active_page':'request'}
    return render (request , 'nurse/donationrequest.html' , context)

def CheckRequest(request , pk):
    questions = None
    answer = None
    status = 'Good'
    gender = None

    # Since URL pattern uses <uuid:pk>, pk is already a UUID object
    # No need to validate again as Django has already validated it
    # Just ensure it's a valid UUID object
    if not isinstance(pk, uuid.UUID):
        messages.error(request, 'Invalid request ID format.')
        return redirect('/donorrequest/all')  # Redirect to a safe page

    try:
        # Get all donation request questions
        questions = DonationRequestQuestion.objects.all()
    except:
        questions = None
    try:
        # Prefetch related answers to avoid multiple queries
        answer = DonationRequestFormResult.objects.prefetch_related('answers__question').get(Result_id = pk)
    except:
        answer = None

    try:
        # Get the donor to determine gender
        # Donor_id is a foreign key to the Donor model, so we can access the donor directly
        donor = answer.Donor_id
        # If donor is None, it means the foreign key was set to NULL
        if donor is None:
            print("Donor record not found for this request")
            status = 'Notgood'
            raise Exception("Donor record not found")

        gender = donor.Gender

        # Get all answers for this request result
        answers = answer.answers.all()  # Using the related manager from the foreign key

        # Check if there are any answers at all
        if not answers.exists():
            # If there are no answers, donor is not eligible (form not properly filled)
            status = 'Notgood'
        else:
            # Check if any answered question is 'yes', which indicates a health concern
            for answer_obj in answers:
                try:
                    # Get the question associated with this answer
                    question = answer_obj.question

                    # Skip gender-specific questions if donor is not of required gender
                    if question.is_gender_specific and gender != question.gender_required:
                        continue

                    # A 'yes' answer indicates a health concern that makes the donor not eligible
                    # Only 'no' answers indicate eligibility
                    if answer_obj.answer == 'yes':
                        status = 'Notgood'
                        break
                    # If answer is null/empty, we should investigate further
                    # For now, treat empty answers as a reason for ineligibility for safety
                    elif answer_obj.answer is None or (hasattr(answer_obj.answer, 'strip') and answer_obj.answer.strip() == ''):
                        status = 'Notgood'
                        break
                except Exception as e:
                    print(f"Error processing answer {answer_obj.answer_id}: {e}")
                    status = 'Notgood'  # Set to not eligible if there's an error processing an answer
                    break

    except Exception as e:
        status = 'Notgood'  # Default to not eligible if there's an error getting donor info
        print(f"Error determining status: {e}")

    # Prepare a list of tuples (question, answer) for easier display in template
    question_answer_pairs = []
    if hasattr(answer, 'answers'):
        # Create a mapping of question_id to answer for quick lookup
        answer_map = {}
        for answer_obj in answer.answers.all():
            try:
                answer_map[str(answer_obj.question.pk)] = answer_obj.answer
            except Exception as e:
                print(f"Error mapping answer {answer_obj.answer_id} to question: {e}")
                continue

        # Create pairs of questions and their answers
        for question in questions:
            # Skip gender-specific questions if donor is not of required gender
            if question.is_gender_specific and gender != question.gender_required:
                continue
            try:
                answer_text = answer_map.get(str(question.pk), "No answer provided")
                question_answer_pairs.append((question, answer_text))
            except Exception as e:
                print(f"Error creating pair for question {question.question_id}: {e}")
                continue

    print(status)
    context = {
        'account': Userstate(request)['account'],
        'questions': questions,
        'answers': answer,
        'question_answer_pairs': question_answer_pairs,  # Pass the question-answer pairs to the template
        'status': status,
        'gender': gender,
        'active_page': 'request'
    }
    return render(request, 'nurse/checkrequest.html', context)

def CheckAppointments(request , type):
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
                if(searchby == 'DonorName'):
                    dn = Donor.objects.get(Donorname = searched)
                    appointment = Appointment.objects.filter(Donor_id = dn.Donor_id)
                elif(searchby == 'Phone'):
                    addr = Address.objects.get(Phone = int(searched))
                    dn = Donor.objects.get(Address_id = addr)
                    appointment = Appointment.objects.filter(Donor_id = dn.Donor_id)
                elif(searchby == 'Date'):
                    date = parse_date(searched)
                    appointment = Appointment.objects.filter(Date =  date)
                elif(searchby == 'Status'):
                    appointment = Appointment.objects.filter(status =  searched.lower())

    except:
        appointment = None
    context = {'account': Userstate(request)['account'] ,'type':type ,  'appointments':appointment , 'active_page':'appointment'}
    return render (request , 'nurse/appointment.html' , context)

def Confirmrequest(request ,  pk , type):
    # Since URL pattern uses <uuid:pk>, pk is already a UUID object
    # Just ensure it's a valid UUID object
    if not isinstance(pk, uuid.UUID):
        # If pk is not a valid UUID, return an error
        messages.error(request, 'Invalid request ID format.')
        return redirect('/donorrequest/all')

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
     context = {'account': Userstate(request)['account'] , 'active_page':'appointment'}
     return render(request , 'nurse/appointment.html' , context)
        



def GetDonorAddress(request , pk , sender ):
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
    context = {'account': Userstate(request)['account'] , 'sender':sender ,'address':address , 'donor':acc , 'active_page':'request' }
    return render(request , 'nurse/checkdonoraddress.html' , context)

def DonorQuestions(request , type):
    questions = None
    try:
        if(type == 'all'):
            questions = DonationRequestQuestion.objects.all()
        else:
            questions = DonationRequestQuestion.objects.all()[0:3]
    except:
        questions = None
    context = {'account':Userstate(request)['account'] , 'type':type ,'questions':questions , 'active_page':'question'}
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
    context = {'account':Userstate(request)['account'] , 'form':form , 'type':type , 'active_page':'question'}
    return render(request , 'nurse/addquestions.html' , context)

# def AddAppointmentDate(request , type):
#     form = AppointmentChoiceCreationForm()
#     if request.method == 'POST':
#         form = AppointmentChoiceCreationForm(request.POST)
#         if (form.is_valid()):
#             try:
#                 form.save()
#                 messages.success(request, 'Appointment Date Added Sucessfuly')
#                 return redirect('/appointmentchoices/notall')
#             except:
#                 messages.error(request, 'Error during adding Appointment Date')
#         else:
#             messages.error(request, 'Error during adding Appointment Date')
#     context = {'account':Userstate(request)['account'] , 'form':form , 'type':type}
#     return render(request , 'nurse/addappointmentchoice.html' , context)

# def AppointmentChoices(request , type):
#     choices = None
#     try:
#         if(type == 'all'):
#             choices = AppointmentChoice.objects.all()
#         elif(type == 'notall'):
#             choices = AppointmentChoice.objects.all()[0:3]
#         elif(type=='searched'):
#             if request.method == 'POST':
#                 searchby = request.POST['searchby']
#                 searched = request.POST['searched']
#                 if(searchby == 'Date'):
#                     date = parse_date(searched)
#                     choices = AppointmentChoice.objects.filter(Date = date)
#                 elif(searchby == 'Time'):
#                     time = parse_time(searched)
#                     choices = AppointmentChoice.objects.filter(Time = time)
#                 elif(searchby == 'DonorsNo'):
#                     choices = AppointmentChoice.objects.filter(NumberofDonors = int(searched))
#     except:
#         choices = None
#     context = {'account':Userstate(request)['account'] , 'type':type ,  'choices':choices }
#     return render (request , 'nurse/appointmentchoices.html' , context)

# def UpdateAppointmentChoice(request , pk ):
#     appointmentchoice = AppointmentChoice.objects.get(Appchoice_id=pk)
#     form = AppointmentChoiceCreationForm (instance= appointmentchoice)
#     if request.method == 'POST':
#         form = AppointmentChoiceCreationForm(request.POST, instance=appointmentchoice)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Appointment choice was updated successfully!')
#             return redirect('/appointmentchoices/notall')
#         else:
#             messages.success(request, 'Appointmentchoice was not updated successfully!')

#     context = {'form': form , 'type':'update' , 'account':Userstate(request)['account']}
#     return render(request, 'nurse/addappointmentchoice.html', context)
            
# def DeleteAppointmentChoice(request , pk):
#     appointmentChoice = AppointmentChoice.objects.get(Appchoice_id=pk)
#     try:
#         appointmentChoice.delete()
#         messages.success(request, 'Appointment Choice was deleted successfully!')
#         return redirect('/appointmentchoices/notall')
#     except:
#         messages.success(request, 'Appointment Choice was not deleted successfully!')
#     return render(request, 'nurse/appointmentchoices.html' , context)


def UpdateQuestion(request , pk ):
    question = DonationRequestQuestion.objects.get(question_id=pk)
    form = DonationRequestQuestionForm(instance=question)
    if request.method == 'POST':
        form = DonationRequestQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question was updated successfully!')
            return redirect('/donorquestions/all')
        else:
            messages.success(request, 'Question was not updated successfully!')

    context = {'form': form , 'type':'update' , 'account':Userstate(request)['account'] , 'active_page':'question'}
    return render(request, 'nurse/addquestions.html', context)

def DeleteQuestion(request , pk):
    question = DonationRequestQuestion.objects.get(question_id=pk)
    try:
        question.delete()
        messages.success(request, 'question was deleted successfully!')
        return redirect('/donorquestions/all')
    except:
        messages.success(request, 'question was not deleted successfully!')
    return render(request, 'nurse/donorquestions.html' , {'active_page':'question'})


