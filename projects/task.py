from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

@shared_task
def send_project_invitation(email, domain, sender_username, token, ignore_result=True):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return

    relative_verification_url = reverse('verify_project_invite', kwargs={'token': token})
    verification_url = f"http://{domain}{relative_verification_url}"
    subject = 'Project invitation'
    message = f'Hi {user.username}, please click on the link to get access to the project created by {sender_username}: {verification_url}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)