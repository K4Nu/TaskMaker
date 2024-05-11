from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.form,name="form"),
    path("delete_task/<int:task_id>/",views.delete_task,name="delete_task"),
    path("edit_task/<int:task_id>/",views.edit_task,name="edit_task"),
    path("mark_as_done/<int:task_id>",views.mark_as_done,name="mark_as_done"),
]