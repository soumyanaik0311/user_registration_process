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


class PasswordResetOTPForm(forms.Form):
    username = forms.CharField(max_length=150)
    otp = forms.CharField(max_length=6)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data