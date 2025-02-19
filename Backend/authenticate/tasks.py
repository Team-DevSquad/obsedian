import os
from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import send_mail
import random
from .models import User
from django.template import loader
from django_celery_beat.models import PeriodicTask
from obsedianguard.celery import app
from celery import Celery

@shared_task(bind=True)
# @app.task
def sendEmailTask(self,email):
    subject="✅ Verify Your Obsidian Account Now! 🔒"
    otp=random.randint(100000,999999)
    html_message = loader.render_to_string('email/verify_email.html',{'otp':otp})
    send_mail(subject,"", 'Obsedian Admin', [email], fail_silently=False,html_message=html_message)
    user_obj=User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()
    return f"Verification Email send to: {email} ✅"

# Task for sending email for resetting password
@shared_task(bind=True)
def sendForgotEmailTask(self, email):
    subject="🔄 Reset Your Obsidian Password in a Snap! 🔐"
    otp=random.randint(100000,999999)
    html_message = loader.render_to_string('email/forgot_password.html',{'otp':otp})
    send_mail(subject,"", 'Obsedian Admin', [email], fail_silently=False,html_message=html_message)
    user_obj=User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()
    return f"Forgot Password Email send to: {email} ✅"

@shared_task(bind=True)
def sendScheduleEmailTask(self,email):
    subject="🔑 Your Obsidian Account Verification Code is Here! 🚀"
    otp=random.randint(100000,999999)
    html_message = loader.render_to_string('email/forgot_password.html',{'otp':otp})
    send_mail(subject,"", 'Obsedian Admin', [email], fail_silently=False,html_message=html_message)
    return "DONE"

# to set otp invalid after 5 minutes of sending to user
@shared_task(bind=True)
def invalidateOTP(self,email,name):
    user_obj=User.objects.get(email=email)
    user_obj.otp_validity=False
    user_obj.save()
    periodic_task = PeriodicTask.objects.get(name=name)
    periodic_task.enabled = False
    periodic_task.save()
    return f"SET otp Invalid for {email} ✅"

# Task for sending email to subscribed users
@shared_task(bind=True)
def sendSubscriptionEmailTask(self, email):
    subject="🛡️ Top Strategies to Supercharge Your Organization’s Security! 💪"
    html_message = loader.render_to_string('email/subscription_email.html',{'otp':'otp'})
    send_mail(subject,"", 'Obsedian Blog', [email], fail_silently=False,html_message=html_message)
    # write code to tell that email is sent
    # user_obj=User.objects.get(email=email)
    # user_obj.otp=otp
    # user_obj.save()
    return f"Subscription Email send to: {email} ✅"

# Task for sending email for marketing
@shared_task(bind=True)
def sendMarketingEmailTask(self, email):
    subject="🔐✨ Unlock the Power: Your Organization’s Security Key is Here! 🚀🔑" 
    html_message = loader.render_to_string('email/marketing_email.html',{'otp':'otp'})
    send_mail(subject,"", 'Obsedian Blog', [email], fail_silently=False,html_message=html_message)
    # write code to tell that email is sent
    # user_obj=User.objects.get(email=email)
    # user_obj.otp=otp
    # user_obj.save()
    return f"Marketing Email send to: {email} ✅" 


# Task to send Valnerability alert 
@shared_task(bind=True)
def sendVulnerabilityEmailTask(self, email):
    subject="⚠️🚨 Critical Alert: Vulnerability Detected in Your Product! 🛡️🔍"
    html_message = loader.render_to_string('email/alert_email.html')
    send_mail(subject,"", 'Obsedian Alert', [email], fail_silently=False,html_message=html_message)
    # write code to tell that email is sent
    # user_obj=User.objects.get(email=email)
    # user_obj.otp=otp
    # user_obj.save()
    return f"Vulnerability Email send to: {email} ✅"


# Task to send invoice email
@shared_task(bind=True)
def sendInvoiceEmailTask(self, email):
    subject="Your Subscription Invoice is Here! 🛡️"
    html_message = loader.render_to_string('email/invoice_email.html')
    send_mail(subject,"", 'Obsedian Billing', [email], fail_silently=False,html_message=html_message)
    # write code to tell that email is sent
    # user_obj=User.objects.get(email=email)
    # user_obj.otp=otp
    # user_obj.save()
    return f"Invoice Email send to: {email} ✅"

# Task to send invoice email
@shared_task(bind=True)
def sendWaitlistEmailTask(self, email):
    subject="Congratulations 🎉 You’re on the Obsidian Waitlist!"
    html_message = loader.render_to_string('email/waitlist_email.html')
    send_mail(subject,"", 'Obsidian Team', [email], fail_silently=False,html_message=html_message)
    # write code to tell that email is sent
    # user_obj=User.objects.get(email=email)
    # user_obj.otp=otp
    # user_obj.save()
    return f"Waitlist joining Email send to: {email} ✅"