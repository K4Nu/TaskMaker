from django.core.mail import send_mail
from django.conf import settings
from django.core.signing import Signer
from django.urls import reverse
import os
import requests

def send_verification_email(user, domain):
    signer = Signer()
    token = signer.sign(user.pk)
    relative_verification_url = reverse('verify_email', kwargs={'token': token})
    verification_url = f"http://{domain}{relative_verification_url}"
    subject = 'Please verify your email'
    message = f'Hi {user.username}, please click on the link to verify your email: {verification_url}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

def image_generation(payload):
    API_URL=os.environ.get("IMAGE_API_URL")
    headers={"Authorization":os.environ.get("IMAGE_KEY")}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def nfsw_filter(payload):
    API_URL=os.environ.get("NFSW_API_URL")
    headers={"Authorization":os.environ.get("NFSW_KEY")}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()