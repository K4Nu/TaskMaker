from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied
class EmailVerifiedBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        user_verified=user.profile.email_verified
        if user and user_verified:
            return user
        elif user and not user_verified:
            raise PermissionDenied("Your email address is not verified")
        return None