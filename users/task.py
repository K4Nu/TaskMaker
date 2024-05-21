from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.signing import Signer
from django.urls import reverse
from django.contrib.auth import get_user_model
import os
@shared_task
def send_verification_email(user_id, domain):
    User=get_user_model()
    user=User.objects.get(pk=user_id)
    signer = Signer()
    token = signer.sign(user.pk)
    relative_verification_url = reverse('verify_email', kwargs={'token': token})
    verification_url = f"http://{domain}{relative_verification_url}"
    subject = 'Please verify your email'
    message = f'Hi {user.username}, please click on the link to verify your email: {verification_url}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_welcome(username,email):
    send_mail(
                'Welcome to To-Do App',
                f'Welcome {username} to our app, we hope you will enjoy it',
                os.environ.get("EMAIL_HOST_USER"),
                [email],
            )
