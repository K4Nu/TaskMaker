from .models import Task,Project,ProjectInvitation
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import TaskForm,ProjectForm,ProjectInvitationForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from .task import send_project_invitation
from django.contrib.sites.shortcuts import get_current_site
import math

@login_required
def create_task(request, project_id=None):
    project = None
    if project_id:
        project = get_object_or_404(Project, id=project_id)
        if not request.user in project.admins.all():
            messages.error(request, "You do not have permission to add tasks to this project.")
            return redirect("my_projects")

    if request.method == "POST":
        form = TaskForm(request.POST, project_id=project_id)
        if form.is_valid():
            task = form.save(commit=False)
            if project:
                task.project = project
            task.save()
            form.save_m2m()  # Save the many-to-many relationships
            messages.success(request, "Task created successfully.")
            if project:
                return redirect("my_projects")
            else:
                return redirect("index")
    else:
        form = TaskForm(project_id=project_id)

    return render(request, "projects/form.html", {"form": form, "project": project})

@require_POST
def delete_task(request,task_id):
    task=Task.objects.get(id=task_id)
    project=task.project
    task.delete()
    if project:return redirect("my_projects")
    return redirect('index')

@login_required
def edit_task(request,task_id):
    task=get_object_or_404(Task,pk=task_id)
    if request.user in task.project.admins.all():
        if request.method=="POST":
            form=TaskForm(request.POST,instance=task)
            if form.is_valid():
                task=form.save()
                return redirect('index')
        else:
            form=TaskForm(instance=task)
    else:
        messages.error("you can not download this")
        return ("index")
    return render(request,"projects/edit_task.html",{"form":form})

#task_mark_as_done
@login_required
def mark_as_done(request,task_id):
    task=Task.objects.get(id=task_id)
    task.status=False
    task.date_end=timezone.now().date()
    task.save()
    return redirect('index')

@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.admins.add(request.user)
            project.users.add(request.user)
            return redirect('my_projects')
    else:
        form = ProjectForm()  # no need to set initial here as model defaults should apply

    return render(request, "projects/project_form.html", {'form': form})

@require_POST
def delete_project(request,project_id):
    project=get_object_or_404(Project,id=project_id)
    if request.user in project.admins.all():
        try:
            with transaction.atomic():
                project.tasks.all().delete()
                project.delete()
                messages.success(request, "Project deleted successfully.")
                return redirect('my_projects')
        except Exception as e:
            messages.error(request, "There was an error deleting the project.")
            return redirect('my_projects')
    else:
        messages.error(request, "You do not have permission to delete this project.")
        return redirect("my_projects")

@login_required
def projects(request):
    projects=Project.objects.filter(users=request.user)
    return render(request,"projects/my_projects.html",{"projects":projects})

@login_required
def project_invitation(request,project_id):
    if request.method=="POST":
        form=ProjectInvitationForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get("email")
            invitation=ProjectInvitation(email=email,project_id=project_id)
            invitation.save()
            domain=get_current_site(request).domain
            send_project_invitation(email,domain,request.user,invitation.token)
            return redirect("my_projects")
        else:
            print(form.errors)
    else:
        form=ProjectInvitationForm()
    return render(request,"projects/project_invite.html",{"form":form})

def verify_project_invite(request,token):
    invite=ProjectInvitation.objects.get(token=token)
    user=User.objects.get(email=invite.email)
    project=Project.objects.get(id=invite.project_id)
    project.users.add(user)
    invite.delete()
    return redirect("index")

@login_required
def project_dashboard(request,project_id):
    project=Project.objects.get(id=project_id)
    today=timezone.now().date()
    total_days=(project.date_end-project.date_start).days
    days_passed=(project.date_end-today).days
    if total_days>0:
        days_percent=math.floor((days_passed/total_days)*100)
    else:
        days_percent=100
    if request.user in project.users.all():
        return render(request,"projects/project.html",{"project":project,"today":today,"percent_passed":days_percent})
    return redirect("my_projects")