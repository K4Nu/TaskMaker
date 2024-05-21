from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("create_task",views.create_task,name="create_task"),
    path("create_task/<int:project_id>/",views.create_task,name="create_task"),
    path("delete_task/<int:task_id>/",views.delete_task,name="delete_task"),
    path("edit_task/<int:task_id>/",views.edit_task,name="edit_task"),
    path("mark_as_done/<int:task_id>",views.mark_as_done,name="mark_as_done"),
    path("create_project",views.create_project,name="create_project"),
    path("my_projects",views.projects,name="my_projects"),
    path("delete_project/<int:project_id>/", views.delete_project, name="delete_project"),
    path("project_invitation/<int:project_id>/",views.project_invitation,name="project_invitation"),
    path("verify_project_invite/<str:token>",views.verify_project_invite,name="verify_project_invite"),
    path("project_dashboard/<int:project_id>",views.project_dashboard,name="project_dashboard")
]

