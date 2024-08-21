from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail

from django.contrib.auth import authenticate,login
from django.urls import reverse

def registration(request):

    UF=UserForm()
    PF=ProfileForm()
    d={'UF':UF,'PF':PF}

    if request.method=='POST'and request.FILES:
        NMUFDO=UserForm(request.POST)
        NMPFDO=ProfileForm(request.POST,request.FILES)
        if NMUFDO.is_valid and NMPFDO.is_valid():
            MFUFDO=NMUFDO.save(commit=False)
            pw=NMUFDO.cleaned_data['password']
            MFUFDO.set_password(pw)
            MFUFDO.save()


            MFPFDO=NMPFDO.save(commit=False)
            MFPFDO.username=MFUFDO
            MFPFDO.save()

            send_mail(
                'Verification mail',
                'Thanks for registration',
                'soumyaranjan.naik.axp@gmail.com',
                [MFUFDO.email],
                fail_silently=False
                )
            
            return HttpResponse('registration is successfull!!')
        else:
            return HttpResponse('Registration Unsuccessfull')


    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):  
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d) #returning home page with login request and session
    return render(request,'home.html')

def user_login(request):

    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid Credentials!!')
    return render(request,'user_login.html')