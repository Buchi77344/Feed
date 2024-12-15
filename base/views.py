from django.shortcuts import render ,get_object_or_404 ,redirect
from .models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth
# Create your views here.
def index(request):
    return render (request, 'index.html')

def signup(request):
    if request.method == "POST":
        first_name =request.POST.get('first_name')
        last_name =request.POST.get('last_name')
        email =request.POST.get('email')
        phone_nummber =request.POST.get('phone_nummber')
        password =request.POST.get('password')
        password1 =request.POST.get('password1')
        if password == password1:
            if User.objects.filter(phone_nummber=phone_nummber).exists:
                messages.error(request, 'Phone Number already exist ')
                return redirect('signup')
            if User.objects.filter(email=email).exists:
                messages.error(request, 'email already exist ')
                return redirect('signup')
            else:
               User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=email,phone_nummber=phone_nummber,password=password)
               messages.success(request, 'Account Created')
               return redirect('login')
        else:
             messages.error(request, 'Password do not match ')
             return redirect('signup')
    else:
        return render (request, 'signup,hrml')
    

def login (request):
    if request.method == "POST":
        email = request.POST.get('email')
        password =request.POST.get('password')

        user = auth.authenticate(request, username=email,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')

        else:
            messages.error(request, 'invalid Credentials')
            return redirect('login')
    else:

       return render (request, 'login.html')


 


