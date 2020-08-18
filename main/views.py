from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
import bcrypt

# Create your views here.
def display_login_and_register_page(request): #displaying page for login/register // url will be ''
    return render(request, 'index.html')  

def create_user(request):
    errors = User.objects.basic_validator(request.POST)     #validations

    if len(errors) > 0:                   #this is for the validations // if there is more than 1 error you will be redirected to the same page and try again
        for key, err in errors.items():
            messages.error(request, err)
        return redirect('/')

    hashed_pw = bcrypt.hashpw(              #to hash the password
        request.POST['password'].encode(),
        bcrypt.gensalt()
    ).decode()

    created_user = User.objects.create(         #creating the user // attributes 
        first_name= request.POST['first_name'], #orange has to match models
        last_name= request.POST['last_name'],   #yellow has to match name inside of html
        email= request.POST['email'],
        password = hashed_pw,
    )

    request.session['user_id']= created_user.id 
    return redirect('/dashboard')


def login(request):
    potential_users = User.objects.filter(email=request.POST['email']) #email if not just change to username
    if len(potential_users) == 0:
        messages.error(request,"Email is not in our system")    #checking validations
        return redirect('/')                                #will redirect you to the same page
    user = potential_users[0]                               #first user

    if not bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
        messages.error(request, "Please check your email and password")


        return redirect('/')
    
    request.session['user_id'] = user.id    #ADD THE REQUEST.SESSION FROM ABOVE
    return redirect('/dashboard')           #website you want it to go to when you sign in

#############################################################################


def display_dashboard_page(request):                            #will have to take in all jobs // have to get a specific user which comes from the session
    context= {
        "jobs":Job.objects.all(), #COMMA!!
        "user":User.objects.get(id=request.session["user_id"])
    }
    
    return render(request, "dashboard_page.html",context) #create a html for that dashboard page


######### CREATING THE JOB DISPLAY PAGE AND CREATING A JOB ACTION ##########

def create_job_page(request):

    context = {
        "user": User.objects.get(id=request.session["user_id"])
    }

    return render(request, "create_job_page.html", context)


def create_job_action(request):
    errors=Job.objects.basic_validator(request.POST)
    Job.objects.create(
        title=request.POST["title"],
        description=request.POST["description"],
        location=request.POST["location"],
        user=User.objects.get(id=request.session["user_id"])
    )

    return redirect("/dashboard")


######## BELOW IS THE EDIT JOB PAGE //// EDIT JOB ACTION FUNCTION #####
def edit_job_page(request, job_id): #id to know which job
    job=Job.objects.get(id=job_id)      #creating a variable 

    context={
        "job": job, #refering to the variable
        "user":User.objects.get(id=request.session["user_id"]) #including session user id // we need a specific user
    }
    return render(request, "edit_page.html", context) #creating html 

def edit_job_action(request, job_id):
    errors=Job.objects.basic_validator(request.POST)        #validations

    if len(errors) >0:
        for err in errors.values():
            messages.error(request, err)
        return redirect(f"/jobs/edit/{job_id}")     #f string bc he need the job id inside the url 
    

    newjob=Job.objects.get(id=job_id)

    newjob.title=request.POST["title"]
    newjob.description=request.POST["description"]
    newjob.location=request.POST["location"]

    newjob.save()
    return redirect("/dashboard")

#######################################################################

def view_job_page(request, job_id):
    context={
        "job": Job.objects.get(id=job_id),
        "user": User.objects.get(id=request.session["user_id"])
    }
    return render(request, "view_job_page.html", context)


################# DELETE ##################
def delete(request, job_id):                #deleting the specific job id
    job=Job.objects.get(id=job_id)
    job.delete()                        #dont forget

    return redirect("/dashboard")   