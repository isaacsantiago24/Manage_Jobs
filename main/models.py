from django.db import models
import re 


class UserManager(models.Manager):
    def basic_validator(self, data):        #data
        errors = {}         #errors dictionary

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #for email

        if len(data['first_name']) <1:                                      #validations
            errors['first_name'] = 'Please enter your first name!'

        if len(data['last_name']) <1:
            errors['last_name'] = 'Please enter your last name!'

        if len(data['email']) <1:
            errors['email'] = 'Please enter your email!'

        elif not EMAIL_REGEX.match(data['email']):                  #else if for email
            errors['email'] = 'Please enter a valid email address!'

        if len(data['password'])< 8:
            errors['password'] = 'Please enter at least 8 characters for your password!'

        if data['pw_confirm'] != data['password']:
            errors['pw_confirm'] = 'Please match your password to its confirmation!'

        return errors

        
class JobManager(models.Manager): ####### MANAGER NOT MODEL ####     #for the class job validations
    def basic_validator(self, data):
        errors = {}

        if len(data['title']) <3:
            errors['title'] = 'Please enter a title!'

        if len(data['description']) <3:
            errors['description'] = 'Please a valid description!'

        if len(data['location']) <4:
            errors['location'] = 'Please enter a location!'

        return errors
        


class User(models.Model):
    first_name=models.CharField(max_length=60)
    last_name=models.CharField(max_length=60)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=30)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects=UserManager()   ##dont forget to create objects




class Job(models.Model):
    title=models.CharField(max_length=70)
    description=models.TextField(max_length=200)
    location=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    user=models.ForeignKey(User, on_delete=models.CASCADE)  
    #one to many you put the foreign key on the many side. 1 user has many jobs

    objects=JobManager()######DONT FORGET TO ADD AFTER ADDING SECOND VALIDATIONS ####
