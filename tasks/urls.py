from django.urls import path
from . import views

app_name = 'tasks'
urlpatterns = [
    path("", views.tasks_view, name="task_list"),
    path("admin_task_list/", views.admin_tasks_view, name="admin_task_list"),
    path("<id>/task_edit/", views.task_edit_view, name="task_edit"),
    path("<id>/task_delete/", views.task_delete_view, name="task_delete"),
]
