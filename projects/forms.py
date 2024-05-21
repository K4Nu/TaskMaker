from django import forms
from .models import Task,Project,ProjectInvitation
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

"""
Add clean for color
"""


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'date_start', 'date_end', 'color']
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_date_start(self):
        date_start = self.cleaned_data.get("date_start")
        if date_start and date_start < timezone.now().date():
            raise forms.ValidationError("The start date cannot be in the past.")
        return date_start

    def clean_date_end(self):
        date_start = self.cleaned_data.get("date_start")
        date_end = self.cleaned_data.get("date_end")
        if date_end and date_end < timezone.now().date():
            raise forms.ValidationError("The end date cannot be in the past.")
        if date_start and date_end and date_end < date_start:
            raise ValidationError("The end date cannot be earlier than the start date.")
        return date_end

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "content", "date_start", "date_end"]
        widgets = {
            'date_start': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_end': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_date_start(self):
        date_start = self.cleaned_data.get("date_start")
        if date_start and date_start < timezone.now().date():
            raise forms.ValidationError("The start date cannot be in the past.")
        return date_start

    def clean_date_end(self):
        date_start = self.cleaned_data.get("date_start")
        date_end = self.cleaned_data.get("date_end")
        if date_end and date_end < timezone.now().date():
            raise forms.ValidationError("The end date cannot be in the past.")
        if date_start and date_end and date_end < date_start:
            raise ValidationError("The end date cannot be earlier than the start date.")
        return date_end


class ProjectInvitationForm(forms.ModelForm):
    class Meta:
        model=ProjectInvitation
        fields=["email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User with this email does not exist")
        return email