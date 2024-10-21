from django.core.mail import EmailMessage
from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User, OneTimePassword
from django.contrib.sites.shortcuts import get_current_site


def generatedotp(): 
    otp=random.randint(1000, 9999)
    return otp
    
def send_code_to_user(email):
    subject="One time password for Email Verification"
    otpcode=generatedotp()
    print(otpcode)
    user = User.objects.get(email=email)
    email_body=f"Hi {user.first_name} thanks for signing up on  please verify your email with the \n one time passcode {otpcode}"

    otp_obj=OneTimePassword.objects.create(user=user, otp=otpcode)
      #send the email 
    d_email=EmailMessage(subject=subject, body=email_body, from_email='sharathshet.n@gmail.com', to=[user.email])
    d_email.send()

    return otp_obj


def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )
    email.send()

    

# def send_normal_email(data):
#     email=EmailMessage(
#         subject=data['email_subject'],
#         body=data['email_body'],
#         from_email=settings.EMAIL_HOST_USER,
#         to=[data['to_email']]
#     )
#     email.send()