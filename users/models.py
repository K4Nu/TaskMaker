from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from PIL import Image,ImageEnhance
from django.core.exceptions import ValidationError

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.user.username)}.{ext}"
    return f'profile_pics/{filename}'

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(default="default.jpg",upload_to=user_directory_path)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        try:
            image=Image.open(self.image.path)
            max_size=(320,320)
            image.thumbnail(max_size,Image.LANCZOS)
            image.save(self.image.path)
        except IOError as e:
            return ValidationError(f"Error processing image {e}")
        except Exception as e:
            return ValidationError(f'Unexpected error {e}')

class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="notification")
    text=models.CharField(max_length=256)
    status=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.status=True
        self.save()