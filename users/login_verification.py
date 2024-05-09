from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
User = get_user_model()

class EmailNotVerifiedException(PermissionDenied):
    """Exception raised when the email has not been verified."""
    pass

class EmailVerifiedBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if not user:
            raise PermissionDenied("Not user")
        user_verified=user.profile.email_verified
        if user and user_verified:
            return user
        """
        elif user and not user_verified:
            raise PermissionDenied("Your email address is not verified")
        """
        return None