from django.shortcuts import render,redirect
from . import models  # import model is important 
from django.contrib import messages
from django.shortcuts import render, HttpResponse

#Get
def index(request):
    return render(request, "index.html")  


def LoginUser(request):
    if request.method == "POST": 
        errors = models.User.objects.basic_validator_login(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/')          
        else: 
            user1 = models.user_login(request)
            if user1 is not False:     
                print("Logged in sucessfully")            
                return redirect('/Home')  
            else:
                print("Not logged in successfully")   
                return redirect('/')        
    print("Not Post requet")
    return redirect('/')   

def SaveUser(request):
    if request.method == "POST": 
        errors = models.User.objects.basic_validator_reg(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/')          
        else: 
            models.save_user(request)
            return redirect('/Home')  

#Get
def home(request):
    print("Here")
    if 'loggedin' in request.session:
        context = {
            "AllPies": models.get_allPies(request)
        }  
        return render(request, "home.html", context) 
    else:
        print("Not logged in") 
        return redirect('/') 

def logout(request):
    if 'email' in request.session:
        del request.session['email']
        del request.session['loggedin']
        del request.session['firstname'] 
        del request.session['lastname'] 
        del request.session['user_id'] 
        print("Delete Session, Logout")     
    return redirect('/')   



def SavePie(request):
    if request.method == "POST":  
        errors = models.Pie.objects.basic_validator_save_Pie(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            return redirect('/Home')          
        else: 
            models.save_pie(request)
            return redirect('/Home')

def DeletePie(request, id):
    models.remove_pie(id),  
    return redirect('/Home') 


#Get
def UpdatePie(request, id):
    if 'loggedin' in request.session:
        context = {
            "updatepie": models.update_pie(id),
        }  
        return render(request, "Updatepie.html", context)  
    else:
        print("Not logged in") 
        return redirect('/') 

def UpdatePieData(request):
    if request.method == "POST":
        errors = models.Pie.objects.basic_validator_save_Pie(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("Errors") 
            #print('/Update/'+request.POST['id'])
            return redirect('/Update/'+request.POST['id'])          
        else: 
            models.update_pie_data(request)
            return redirect('/Home')

def Allpies(request):
    if 'loggedin' in request.session:
        context = {
            "allpies": models.allpies(),
        }  
        return render(request, "Allpies.html", context)  
    else:
        print("Not logged in") 
        return redirect('/') 

#Get
def ShowPie(request, id):
    if 'loggedin' in request.session:
        context = {
            "showpie": models.show_pie(id),
            "Delornot": models.isDeleciuos(request, id)
        }  
        return render(request, "showpie.html", context)  
    else:
        print("Not logged in") 
        return redirect('/') 

def Vote(request):
    if 'loggedin' in request.session:
        models.Votepie(request)
        return redirect('/AllPies')
    else:
        print("Not logged in") 
        return redirect('/') 