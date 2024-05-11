from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class EmailVerifiedBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user:
            profile = Profile.objects.filter(user=user).first()
            if profile and profile.email_verified:
                return user
        return None
