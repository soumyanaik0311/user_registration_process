from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse

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
            return HttpResponse('registration is successfull!!')
        else:
            return HttpResponse('Registration Unsuccessfull')


    return render(request,'registration.html',d)