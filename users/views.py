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
    CustomAuthenticationForm,
    ImageGenerationForm
)
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer, BadSignature
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
#from task.models import Task
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .utils import send_verification_email,image_generation
from django.utils.timezone import now

def index(request):
    if request.user.is_anonymous:
        return render(request,"users/landing.html")
    """
    tasks = Task.objects.filter(status=True, date_end__gte=timezone.now(),user=request.user).order_by('date_end')
    paginator=Paginator(tasks,9)
    page=request.GET.get("page")
    try:
        tasks=paginator.page(page)
    except PageNotAnInteger:
        tasks=paginator.page(1)
    except EmptyPage:
        tasks.paginator.page(paginator.num_pages)
    """
    return render(request,"users/index.html")

def register(request):
    from django.apps import apps
    print(apps.is_installed('crispy_forms'))
    print(apps.is_installed('crispy_bootstrap5'))
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
            send_verification_email(user,domain)
            return render(request,"users/verification.html")
    else:
        form=CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    #current=Task.objects.filter(user=request.user,status=True)
    #done = Task.objects.filter(user=request.user, status=False)
    return render(request, "users/profile.html")#{"current":current,"done":done})

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
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.profile.email_verified:
                    login(request, user)
                    return redirect('index')  # Redirect to a success page.
                else:
                    messages.error(request, "Your email address is not verified.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def generate_image(request):
    if request.method == "POST":
        form = ImageGenerationForm(request.POST)
        if form.is_valid():
            try:
                filename = "test.png"
                filepath = os.path.join("media", filename)
                input_data = form.cleaned_data.get("input")

                image_data = image_generation({"inputs": input_data})
                image = Image.open(io.BytesIO(image_data))
                image.thumbnail((512, 512), Image.Resampling.LANCZOS)
                image.save(filepath, "PNG")

                timestamp = now().strftime("%Y%m%d%H%M%S")
                image_url = os.path.join('/media/', filename) + f"?{timestamp}"
                return JsonResponse({'success': True, 'image_url': image_url}, status=200)
            except Exception as e:
                return JsonResponse({'success': False, 'error': f"An error occurred: {str(e)}"}, status=500)
        else:
            errors={field:error.get_json_data() for field,error in form.errors.items()}
            print(errors)
            return JsonResponse({"success":False,"errors":errors},status=400)
    else:
        form = ImageGenerationForm()
    return render(request, "users/generate_image.html", {"form": form})