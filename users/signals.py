from django.db.models.signals import post_save,pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile
from django.core.files.storage import default_storage
import os
from PIL import Image, ImageEnhance
import io
from django.core.files.base import ContentFile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome to To-Do App',
            f'Welcome {instance.username} to our app, we hope you will enjoy it',
            os.environ.get("EMAIL_HOST_USER"),
            [instance.email],
        )
        if instance.is_superuser:
            Profile.objects.create(user=instance,image="admin.png",email_verified=True)

@receiver(pre_save, sender=Profile)
def delete_old_image(sender, instance, **kwargs):
    if instance._state.adding and not instance.pk:
        return
    try:
        old_instance = Profile.objects.get(pk=instance.pk)
    except Profile.DoesNotExist:
        # If there's no old instance, there's nothing to do.
        return

    # Check if the instance has an image, and it's different from the old one.
    if instance.image and old_instance.image != instance.image:
        if old_instance.image and default_storage.exists(old_instance.image.name):
            old_instance.image.delete(save=False)