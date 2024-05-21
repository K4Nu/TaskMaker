import os.path
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django import forms
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    image=forms.FileField(required=False)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email=self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already used")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean(self):
        cleaned_data=super().clean()
        password1=cleaned_data.get("password1")
        username=cleaned_data.get("username")

        if password1 and username and username.lower() in password1.lower():
            self.add_error("password1", "Password cannot contain the username!")

        return cleaned_data

    def clean_image(self):
        image=self.cleaned_data.get("image")
        if image:
            extension=os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.png', '.jpg', '.jpeg']
            if image.size>int(eval(os.environ.get("MAX_UPLOAD_SIZE"))):
                raise forms.ValidationError(f"File size is too big, maximum allowed size is {round(settings.MAX_UPLOAD_SIZE / (1024 * 1024))} MB")
            if extension not in valid_extensions:
                raise forms.ValidationError("Unsupported file extension. Allowed extensions are: PNG, JPG, JPEG.")
        return image

class UpdateUserForm(forms.ModelForm):
    username=forms.CharField(max_length=100,required=True)
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=["username","email"]

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=["image"]
        widgets={"image":forms.FileInput()}

    def clean_image(self):
        image=self.cleaned_data.get("image")
        if image:
            extension=os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.png', '.jpg', '.jpeg']
            if image.size>int(eval(os.getenv('MAX_UPLOAD_SIZE'))):
                raise forms.ValidationError(f"File size is too big, maximum allowed size is {round(settings.MAX_UPLOAD_SIZE / (1024 * 1024))} MB")
            if extension not in valid_extensions:
                raise forms.ValidationError("Unsupported file extension. Allowed extensions are: PNG, JPG, JPEG.")
        return image

class ResendVerificationEmailForm(forms.Form):
    email=forms.EmailField(label="Your email address")

class CustomLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user=User.objects.filter(username=username).first()
        if user is None or not user.profile.email_verified:
            raise forms.ValidationError("Please verify email address")
        elif not authenticate(username=username, password=password):
            raise forms.ValidationError("Invalid username or password")
        return cleaned_data