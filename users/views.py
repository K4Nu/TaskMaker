import os.path
from PIL import Image
import io
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import (
    CustomUserCreationForm,
    UpdateUserForm,
    UpdateProfileForm,
    ResendVerificationEmailForm,
    CustomLoginForm
)
from .models import Profile,Notification
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer, BadSignature
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from projects.models import Task
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .task import send_verification_email,send_welcome
from django.utils.timezone import now
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def index(request):
    if request.user.is_anonymous:
        return render(request,"users/landing.html",{"today":now().date()})
    tasks = Task.objects.filter(status=True, date_end__gte=timezone.now(),assigned_users=request.user).order_by('date_end')
    return render(request,"users/index.html", {"tasks":tasks})

def register(request):
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            profile_image=form.cleaned_data.get("image")
            if not profile_image:
                profile_image="default.jpg"
            profile=Profile(user=user,image=profile_image)
            profile.save()
            current_site=get_current_site(request)
            domain=current_site.domain
            send_verification_email.delay(user.id,domain)
            send_welcome.delay(user.username,user.email)
            return render(request,"users/verification.html")
    else:
        form=CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    current=Task.objects.filter(assigned_users=request.user,status=True)
    done = Task.objects.filter(assigned_users=request.user, status=False)
    return render(request, "users/profile.html",{"current":current,"done":done})

@login_required
def profile_update(request):
    user = request.user
    profile = user.profile

    if request.method=="POST":
        user_form=UpdateUserForm(request.POST,instance=user)
        profile_form=UpdateProfileForm(request.POST,request.FILES,instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            saved_profile=profile_form.save(commit=False)
            saved_profile.save()
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = UpdateProfileForm(instance=profile)

    return render(request, "users/update_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })

def verify_email(request,token):
    signer=Signer()
    try:
        user_id=signer.unsign(token)
        user=User.objects.get(pk=user_id)
        profile=Profile.objects.get(user=user)
        profile.email_verified=True
        profile.save()
        return redirect('login')
    except (BadSignature, User.DoesNotExist,Profile.DoesNotExist):
        return render(request,"users/invalid_token.html")

def resend_verification_email(request):
    if request.method == "POST":
        form = ResendVerificationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                if not user.profile.email_verified:
                    current_site = get_current_site(request)
                    domain = current_site.domain
                    send_verification_email(user,domain)
                    messages.success(request, "A new verification email has been sent to your email address.")
                else:
                    messages.info(request, "Your email is already verified.")
                return render(request,"users/verification.html")
            except User.DoesNotExist:
                messages.error(request, "No user found with this email address.")
    else:
        form = ResendVerificationEmailForm()

    # This return will handle both GET requests and POST requests where the form is not valid or an exception occurs
    return render(request, 'users/resend_verification_email.html', {'form': form})



def custom_login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.profile.email_verified:
                    login(request, user)
                    messages.success(request, "Successfully logged in.")
                    return redirect('index')
        else:
            print(form.errors)
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})

def notify_project_users(request,task):
    project=task.project
    users=project.users.all()

    message=f'Task {task.title} is being completed by {request.user}'

    for user in users:
        if user!=request.user:
            Notification.objects.create(
                user=user,
                text=message
            )
    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"project_{project.id}_notifications",
        {"type":"send_notification",
         "notification":message
         }
    )