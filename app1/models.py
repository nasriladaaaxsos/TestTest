from pickle import FALSE, TRUE
from sqlite3 import Date
from django.db import models
from datetime import datetime
from django.contrib import messages
from django.shortcuts import render,redirect
import bcrypt
import re
from datetime import timedelta, date

class UserManager(models.Manager):
    def basic_validator_login(self, postData):
        errors = {}
        all_user = User.objects.filter(email = postData['email'])
        # add keys and values to errors dictionary for each invalid field
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"    
        if len(postData['email']) == 0 :   
            errors["emailrequired"] = "Email is required!"  
        if len(postData['password']) == 0 :   
            errors["passwordrequired"] = "Password is required!"    
        if len(all_user) and not bcrypt.checkpw(postData['password'].encode(), all_user[0].password.encode()):
            errors["passwordwronge"] = "Wrong Password!"   
        if not len(all_user):
            errors['emailnewuser'] = "Email is not registered" 
        return errors

    def basic_validator_reg(self, postData):
        errors = {}
        new_user = User.objects.filter(email = postData['email'])
        # add keys and values to errors dictionary for each invalid field       
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"  
        if len(postData['confirmpassword']) < 8:
            errors["confirmpassword"] = "Confirm Password should be at least 8 characters" 
        if len(postData['lastname']) < 3:
            errors["lastname"] = "Last name should be at least 3 characters" 
        if len(postData['firstname']) < 3:
            errors["firstname"] = "First Name should be at least 3 characters" 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address!"
        if postData['password'] != postData['confirmpassword']:
            errors['password_confirm'] = "Password Dosent Match!"
        if len(postData['email']) == 0 :   
            errors["emailrequired"] = "Email is required!"  
        if len(postData['password']) == 0 :   
            errors["passwordrequired"] = "Password is required!"
        if len(postData['confirmpassword']) == 0 :   
            errors["confirmpasswordrequired"] = "Confrim password is required!"
        if len(postData['lastname']) == 0 :   
            errors["lastnamerequired"] = "Last name is required!"
        if len(postData['firstname']) == 0 :   
            errors["firstnamerequired"] = "First name is required!"   
        if len(new_user):
            errors['emailnewuser'] = "Email already exist" 
        return errors

class PieManager(models.Manager):  
    def basic_validator_save_Pie(self, postData):
        errors = {}
        if len(postData['piename']) == 0 :   
            errors["piename"] = "Pie Name is required!"  
        if len(postData['piefilling']) == 0 :   
            errors["piefilling"] = "Pie filling is required!" 
        if len(postData['piecrust']) == 0 :   
            errors["piecrust"] = "Crust is required!"  
        return errors

class User(models.Model):   
    firstname = models.TextField(max_length=255)
    lastname = models.TextField(max_length=255)
    email = models.CharField(max_length=45)
    password = models.TextField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)    
    objects = UserManager() 

class Pie(models.Model):
    piename = models.TextField(max_length=255)
    piefilling = models.TextField(max_length=255)
    piecrust = models.TextField(max_length=255)
    createdby = models.ForeignKey(User, related_name="users", default=1,on_delete = models.DO_NOTHING)
    voteflag = models.IntegerField()
    Users = models.ManyToManyField(User, related_name="pies")
    objects = PieManager() 

def user_login(formvalue): #request.POST   
        user_exist = User.objects.filter(email=formvalue.POST['email'])
        #print(user_exist.password)
        #print(formvalue.POST['password'].encode() )
        if user_exist:
            logged_user = user_exist[0] 
            if bcrypt.checkpw(formvalue.POST['password'].encode(), user_exist[0].password.encode()):
                print("password match")
                loggedin(formvalue,logged_user )
                return redirect('/Home')
                #messages.success(formvalue, "User successfully Logged")
            else:
                print("failed password")   
                return False            
        else:
            #print(user_exist[0].password)
            print("testtttttt")
            return False      

def save_user(formvalue): #request.POST    
    user_password = formvalue.POST['password']
    hash1 = bcrypt.hashpw(user_password.encode(), bcrypt.gensalt()).decode()
    print(user_password)
    u = User.objects.create(email = formvalue.POST['email'] ,password = hash1 ,created_date=datetime.now(), firstname = formvalue.POST['firstname'], lastname = formvalue.POST['lastname'] )
    formvalue.session['email'] = u.email
    formvalue.session['loggedin'] = 1
    formvalue.session['firstname'] = u.firstname
    formvalue.session['lastname'] = u.lastname
    formvalue.session['user_id'] = u.id

def loggedin(value, logged_user):
    value.session['email'] = value.POST['email']
    value.session['loggedin'] = 1
    value.session['firstname'] = logged_user.firstname
    value.session['lastname'] = logged_user.lastname
    value.session['user_id'] = logged_user.id

def get_allPies(request):
    return Pie.objects.filter(createdby=request.session['user_id'] )

def save_pie(request):
    if request.session.has_key('user_id'):
        userid = request.session['user_id']
        PieUser = User.objects.get(id= request.session['user_id'])
        Pie.objects.create(piename = request.POST['piename'], piefilling=request.POST['piefilling'], piecrust = request.POST['piecrust'], createdby = PieUser, voteflag = 0  )

def remove_pie(id):
    Pie_selected = Pie.objects.get(id=id)
    Pie_selected.delete()

def update_pie(id):
    Pie_ = Pie.objects.get(id=id)
    return  Pie_

def update_pie_data(request):
    Pie_ = Pie.objects.get(id=request.POST['id'])
    Pie_.piename = request.POST['piename']
    Pie_.piefilling = request.POST['piefilling']
    Pie_.piecrust = request.POST['piecrust']
    Pie_.save()

def allpies():
    return Pie.objects.all().order_by("Users")
def show_pie(id):
    Pie_ = Pie.objects.get(id=id)   
    return Pie_

def Votepie(request):
    pieid=request.POST['id']
    print("ggggggggggggggggggggggggggg")
    if isDeleciuos(request, pieid):
        print("in")
        this_pie = Pie.objects.get(id = pieid )
        this_user = User.objects.get(id= request.session['user_id'])
        print(this_user)
        this_pie.voteflag = this_pie.voteflag-1
        this_pie.save()
        this_pie.Users.remove(this_user)
        print("remove recoerd")
    else:
        print("out")
        this_pie = Pie.objects.get(id = request.POST['id'] )
        this_user = User.objects.get(id= request.session['user_id'])
        print(this_user)
        this_pie.voteflag = this_pie.voteflag+1
        this_pie.save()
        this_pie.Users.add(this_user)
        print("to deliocious")


def isDeleciuos(request, id):
    this_pie = Pie.objects.get(id = id )
    this_user = User.objects.get(id= request.session['user_id'])   
    users_ = User.objects.all()
    pielist = this_pie.Users.all()
    counter = len(users_)
    for user in pielist:
        if (user == this_user):
            print(user)
            return TRUE
    return False

