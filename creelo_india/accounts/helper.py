import random
from django.core.mail import send_mail
from django.core import mail
connection = mail.get_connection()
from django.conf import settings
from .models import User

def send_otp_via_email(email):
   print("*************",email)
   subject=f'your account varifaction email'
   otp= random.randint(1000,9999)
   message=f'your otp is {otp}'
   email_from=settings.EMAIL_HOST
   send_mail(subject,message,email_from,[email])
   user_obj=User.objects.get(email=email)
   user_obj.otp=otp
   print("otp>>>>>>>",otp)
   user_obj.save()

def forget_password_send_email(email):
   subject=f'your account varifaction email'
   password_resetotp= random.randint(1000,9999)
   message=f'your otp is {password_resetotp}'
   email_from=settings.EMAIL_HOST
   send_mail(subject,message,email_from,[email])
   user_obj=User.objects.get(email=email)
   user_obj.password_resetotp=password_resetotp
   print("password_resetotp>>>>>>>",password_resetotp)
   user_obj.save()




  
