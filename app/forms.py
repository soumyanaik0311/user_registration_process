from django import forms

from app.models import *

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets={'password':forms.PasswordInput}
class ProfileForm(forms.ModelForm):
    class Meta:
        model=ProfilePic
        fields=['address','profile_pic']