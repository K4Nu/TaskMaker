from django.contrib import admin
from .models import Task

@admin.register(Task)
class ProfileAdmin(admin.ModelAdmin):
    pass
