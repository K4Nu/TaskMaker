from django.shortcuts import render,redirect
from .forms import TaskForm
from .models import Task
from django.utils import timezone

from django.shortcuts import render, redirect
from .forms import TaskForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
def form(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)  # Prepare to save the task, but don't commit yet
            task.save()  # First save to get an ID assigned
            task.users.add(request.user)  # Now that task has an ID, you can add users to it
            return redirect('index')  # Redirect to an index page or some other appropriate view
    else:
        form = TaskForm()

    return render(request, "project/form.html", {"form": form})

@require_POST
def delete_task(request,task_id):
    task=Task.objects.get(id=task_id)
    task.delete()
    return redirect('index')

@login_required
def edit_task(request,task_id):
    task=Task.objects.get(id=task_id)
    if request.method=="POST":
        form=TaskForm(request.POST,instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form=TaskForm(instance=task)
    return render(request,"project/edit_task.html",{"form":form})

@login_required
def mark_as_done(request,task_id):
    task=Task.objects.get(id=task_id)
    task.status=False
    task.date_end=timezone.now().date()
    task.save()
    return redirect('index')

