from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class ProfilePic(models.Model):
    profile_pic=models.ImageField(upload_to='DP')
    address=models.TextField()
    username=models.OneToOneField(User,on_delete=models.CASCADE)
    
    # Add fields for OTP
    otp = models.CharField(max_length=6, blank=True, null=True)



    # otp_created_at = models.DateTimeField(blank=True, null=True)
    
    # def is_otp_expired(self):
    #     """
    #     Check if the OTP is expired. 
    #     Here, we assume OTP is valid for 10 minutes.
    #     """
    #     if self.otp_created_at:
    #         return timezone.now() > self.otp_created_at + datetime.timedelta(minutes=10)
    #     return True

    def __str__(self):
        return self.username.username