from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class BaseModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1500)
    date_start = models.DateField(default=datetime.date.today)
    date_end = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=True)

    class Meta:
        abstract=True

class Project(BaseModel):
    admins=models.ManyToManyField(User,related_name="project_admins")
    users=models.ManyToManyField(User,related_name="project_users")

class Task(BaseModel):
    color=models.CharField(max_length=7,default="#000000")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", null=True)
    assigned_users=models.ManyToManyField(User,related_name="task_users")

class ProjectInvitation(models.Model):
    email=models.EmailField()
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    token=models.CharField(max_length=50,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        if not self.token:
            self.token=get_random_string(50)
        super().save(*args,**kwargs)

