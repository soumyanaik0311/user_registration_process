from django.shortcuts import render

# Create your views here.
import random
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from app.models import *
from app.forms import *


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


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_data(request):
    username=request.session['username']
    UO=User.objects.get(username=username)
    PO=ProfilePic.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_data.html',d)

@login_required
def change_pw(request):
    if request.method=='POST':
        cpw=request.POST['cpw']
        username=request.session['username']
        UO=User.objects.get(username=username)
        UO.set_password(cpw)
        UO.save()
        return HttpResponse('Password has been changed !')
    return render(request,'change_pw.html')






def reset_pw(request):
    if request.method == 'POST':
        if 'send_otp' in request.POST:
            # Step 1: Generate and send OTP
            username = request.POST.get('username')
            # print(f"Received username for OTP: {username}")  # Debugging print


            UO = User.objects.filter(username__iexact=username)[0]
            otp = str(random.randint(100000, 999999))
            PO = ProfilePic.objects.filter(username=UO)[0]
            PO.otp = otp
                # PO.otp_created_at = timezone.now()
            PO.save()

                # Send OTP via email
            send_mail(
                    'Password Reset OTP',
                    f'Your OTP for password reset is {otp}.',
                    settings.EMAIL_HOST_USER,
                    [UO.email],
                    fail_silently=False,
            )
            return HttpResponse('OTP has been sent to your email.')

            

        elif 'verify_otp' in request.POST:
            # Step 2: Verify OTP and Reset Password
            form = PasswordResetOTPForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                otp = form.cleaned_data['otp']
                new_password = form.cleaned_data['new_password']
                
                # print(f"Verifying OTP for user: {username}")  # Debugging print

              
                UO = User.objects.filter(username__iexact=username)[0]
                PO = ProfilePic.objects.filter(username=UO)[0]
                if PO.otp == otp:
                        UO.set_password(new_password)
                        UO.save()
                        PO.otp = None
                        # PO.otp_created_at = None
                        PO.save()
                        return HttpResponse('Password has been reset successfully.')
                else:
                        # print("Invalid OTP or OTP expired")  # Debugging print
                        return HttpResponse('Invalid OTP or OTP expired.')
              
            else:
                return render(request, 'reset_pw.html', {'form': form}) # Render the form with validation errors

    else:
        form = PasswordResetOTPForm()  # Initialize a new, empty form for GET requests or non-submission cases
    return render(request, 'reset_pw.html', {'form': form}) # Render the template with the form






